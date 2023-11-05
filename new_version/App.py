import os
from flask import Flask, request, jsonify, Response
# import Language
import sys
# import ConvertSTRToTXT
import summarizer
sys.path.append('./Summarize')


app = Flask(__name__)
app.debug = True



@app.errorhandler(404)
def invalid_route(e):
    return jsonify({'errorCode': 404, 'message': 'Invalid Input Url'})


@app.errorhandler(400)
def invalid_route(e):
    return jsonify({'errorCode': 400, 'message': 'Bad Request,input json text is not correct'})


@app.errorhandler(500)
def invalid_route(e):
    return jsonify({'errorCode': 500, 'message': 'Internal Server Error'})


@app.route("/ping")
def ping():
    return "This is a api test only"



@app.route("/summarize_fa", methods=["post"])
def summarizing_fa():
    try:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        data = request.get_json(force=True)
        # print(data)
        text = data["text"]
        # text2='"'+'"'+'"'+text+'"'+'"'+'"'
        # print(text)
        # ConvertSTRToTXT.converting(text)
        summarize = summarizer.summarize(text=text,word_count=50)
        # result = obj.handeling()
        # return jsonify({'result': summarize})
        return jsonify({'result': summarize})
    except:
        return "cant summarize"


# @app.route("/predict", methods=["post"])
# def predicting():
#     try:
#         os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#         data = request.get_json(force=True)
#         base64_string = data["base64_string"]
#         obj = Predicting.Detection(base64_string=base64_string)
#         result = obj.handeling()
#         return jsonify({'result': result})
#     except:
#         return "cant predict"
#
#
# @app.route("/objects", methods=["post"])
# def classification():
#     try:
#         os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#         data = request.get_json(force=True)
#         base64_string = data["base64_string"]
#         ImObject = Classification_main.Image_Classification(base64_Image=base64_string)
#         return jsonify({'result': ImObject})
#     except:
#         return "cant predict"


# @app.route("/translate", methods=["post"])
# def translating():
#     try:
#         os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#         data = request.get_json(force=True)
#         src = str(request.args.get('src'))
#         dest = str(request.args.get('dest'))
#         my_dict = {}
#         for key, value in data.items():
#             translated = Language.translation(input_text=value, src=src, dest=dest)
#             my_dict[key] = translated.text
#         return my_dict
#     except:
#         return "cant translate"

# @app.route("/summarize", methods=["post"])
# def summarizing():
#     try:
#         os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#         data = request.get_json(force=True)
#         # print(data)
#         text = data["text"]
#         # text2='"'+'"'+'"'+text+'"'+'"'+'"'
#         # print(text)
#         ConvertSTRToTXT.converting(text)
#         summarize = main.summarize(filename="Summarize/text.txt")
#         # result = obj.handeling()
#         # return jsonify({'result': summarize})
#         return jsonify({'result': summarize})
#     except:
#         return "cant summarize"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=8535 , use_reloader=False)
