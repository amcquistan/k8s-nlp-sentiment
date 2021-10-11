

from flask import Flask, request, jsonify
from textblob import TextBlob


app = Flask(__name__)


@app.route('/sentiment', methods=('POST',))
def sentiment():
    data = request.get_json()
    blob = TextBlob(data['text'])
    return jsonify({
        'text': data['text'],
        'polarity': blob.sentiment.polarity,
        'subjectivity': blob.sentiment.subjectivity
    })

