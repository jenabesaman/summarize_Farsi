from gensim.summarization.pagerank_weighted import pagerank_weighted as _pagerank
from gensim.summarization.textcleaner import clean_text_by_word as _clean_text_by_word
from gensim.summarization.textcleaner import tokenize_by_word as _tokenize_by_word
from gensim.summarization.commons import build_graph as _build_graph
from gensim.summarization.commons import remove_unreachable_nodes as _remove_unreachable_nodes
from gensim.utils import to_unicode
from itertools import combinations as _combinations
from queue import Queue as _Queue

WINDOW_SIZE = 2
INCLUDING_FILTER = ['NN', 'JJ']
EXCLUDING_FILTER = []

def _get_pos_filters():
    return frozenset(INCLUDING_FILTER), frozenset(EXCLUDING_FILTER)

def _get_words_for_graph(tokens, pos_filter=None):
    if pos_filter is None:
        include_filters, exclude_filters = _get_pos_filters()
    else:
        include_filters = set(pos_filter)
        exclude_filters = frozenset([])
    if include_filters and exclude_filters:
        raise ValueError("Can't use both include and exclude filters, should use only one")

    result = []
    for word, unit in tokens.items():
        if exclude_filters and unit.tag in exclude_filters:
            continue
        if (include_filters and unit.tag in include_filters) or not include_filters or not unit.tag:
            result.append(unit.token)
    return result

def _get_first_window(split_text):
    return split_text[:WINDOW_SIZE]

def _set_graph_edge(graph, tokens, word_a, word_b):
    if word_a in tokens and word_b in tokens:
        lemma_a = tokens[word_a].token
        lemma_b = tokens[word_b].token
        edge = (lemma_a, lemma_b)

        if graph.has_node(lemma_a) and graph.has_node(lemma_b) and not graph.has_edge(edge):
            graph.add_edge(edge)

def _process_first_window(graph, tokens, split_text):
    first_window = _get_first_window(split_text)
    for word_a, word_b in _combinations(first_window, 2):
        _set_graph_edge(graph, tokens, word_a, word_b)

def _init_queue(split_text):
    queue = _Queue()
    first_window = _get_first_window(split_text)
    for word in first_window[1:]:
        queue.put(word)
    return queue

def _process_word(graph, tokens, queue, word):
    for word_to_compare in _queue_iterator(queue):
        _set_graph_edge(graph, tokens, word, word_to_compare)

def _update_queue(queue, word):
    queue.get()
    queue.put(word)
    assert queue.qsize() == (WINDOW_SIZE - 1)

def _process_text(graph, tokens, split_text):
    queue = _init_queue(split_text)
    for i in range(WINDOW_SIZE, len(split_text)):
        word = split_text[i]
        _process_word(graph, tokens, queue, word)
        _update_queue(queue, word)

def _queue_iterator(queue):
    iterations = queue.qsize()
    for _ in range(iterations):
        var = queue.get()
        yield var
        queue.put(var)

def _set_graph_edges(graph, tokens, split_text):
    _process_first_window(graph, tokens, split_text)
    _process_text(graph, tokens, split_text)

def _extract_tokens(lemmas, scores, ratio, words):
    lemmas.sort(key=lambda s: scores[s], reverse=True)
    # If no "words" option is selected, the number of sentences is
    # reduced by the provided ratio, else, the ratio is ignored.
    length = len(lemmas) * ratio if words is None else words
    return [(scores[lemmas[i]], lemmas[i],) for i in range(int(length))]
