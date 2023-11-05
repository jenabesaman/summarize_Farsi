import logging
from gensim.summarization.pagerank_weighted import pagerank_weighted as _pagerank
from gensim.summarization.textcleaner import clean_text_by_sentences as _clean_text_by_sentences
from gensim.summarization.commons import build_graph as _build_graph
from gensim.summarization.commons import remove_unreachable_nodes as _remove_unreachable_nodes
from gensim.summarization.bm25 import get_bm25_weights as _bm25_weights
from gensim.models import Word2Vec
from gensim.corpora import Dictionary
from math import log10 as _log10
from hazm import *

logger = logging.getLogger('summa.preprocessing.cleaner')

try:
    from hazm import POSTagger
    tagger = POSTagger(model='resources/postagger.model')
    logger.info("'pattern' package found; tag filters are available for Persian")
    HAS_PATTERN = True
except ImportError:
    logger.info("'pattern' package not found; tag filters are not available for Persian")
    HAS_PATTERN = False

SEPARATOR = r'@'
RE_SENTENCE = re.compile(r'(\S.+?[.!?])(?=\s+|$)|(\S.+?)(?=[\n]|$)', re.UNICODE)  # backup (\S.+?[.!?])(?=\s+|$)|(\S.+?)(?=[\n]|$)
AB_SENIOR = re.compile(r'([A-Z][a-z]{1,2}\.)\s(\w)', re.UNICODE)
AB_ACRONYM = re.compile(r'(\.[a-zA-Z]\.)\s(\w)', re.UNICODE)
AB_ACRONYM_LETTERS = re.compile(r'([a-zA-Z])\.([a-zA-Z])\.', re.UNICODE)
UNDO_AB_SENIOR = re.compile(r'([A-Z][a-z]{1,2}\.)' + SEPARATOR + r'(\w)', re.UNICODE)
UNDO_AB_ACRONYM = re.compile(r'(\.[a-zA-Z]\.)' + SEPARATOR + r'(\w)', re.UNICODE)

def split_sentences(text):
    return (sent_tokenize(text))

def replace_abbreviations(text):
    return replace_with_separator(text, SEPARATOR, [AB_SENIOR, AB_ACRONYM])

def undo_replacement(sentence):
    return replace_with_separator(sentence, r" ", [UNDO_AB_SENIOR, UNDO_AB_ACRONYM])

def replace_with_separator(text, separator, regexs):
    replacement = r"\1" + separator + r"\2"
    result = text
    for regex in regexs:
        result = regex.sub(replacement, result)
    return result

def get_sentences(text):
    te = sent_tokenize(text)
    for each in te:
        yield (each)

def merge_syntactic_units(original_units, filtered_units, tags=None):
    units = []
    for i in range(len(original_units)):
        if filtered_units[i] == '':
            continue

        text = original_units[i]
        token = filtered_units[i]

        if tags :
            try:
                tag = tags[i][1]
            except:
                tag = None
        else:
            tag = None
        sentence = SyntacticUnit(text, token, tag)
        sentence.index = i
        units.append(sentence)
    return units

def join_words(words, separator=" "):
    return separator.join(words)

def clean_text_by_sentences(text):
    original_sentences = split_sentences(text)
    filtered_sentences = [join_words(sentence) for sentence in preprocess_documents(original_sentences)]
    tags = clean_text_by_word(text)
    return merge_syntactic_units(original_sentences, filtered_sentences, tags)

def clean_text_by_word(text, deacc=True):
    text_without_acronyms = replace_with_separator(text, "", [AB_ACRONYM_LETTERS])
    original_words = list(tokenize(text_without_acronyms, to_lower=True, deacc=deacc))
    filtered_words = [join_words(word_list, "") for word_list in preprocess_documents(original_words)]
    if HAS_PATTERN:
        tags = tagger.tag(original_words) # tag needs the context of the words in the text
    else:
        tags = None
    units = merge_syntactic_units(original_words, filtered_words, tags)
    return dict((unit.text,unit) for unit in units)

def tokenize_by_word(text):
    text_without_acronyms = replace_with_separator(text, "", [AB_ACRONYM_LETTERS])
    return tokenize(text_without_acronyms, to_lower=True, deacc=True)
