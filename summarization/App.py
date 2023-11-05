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
        summarize = summarizer.summarize(text=text,word_count=200)
        return jsonify({'result': summarize})
    except:
        return "cant summarize"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=8535 , use_reloader=False)
