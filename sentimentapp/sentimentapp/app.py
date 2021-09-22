import os

import requests

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/sentiment', methods=('POST',))
def analyze_sentiment():
    request_data = request.get_json()

    url = f"http://{os.environ['SENTIMENT_API_DNS']}:{os.environ['SENTIMENT_API_PORT']}/sentiment"
    response = requests.post(url, json={'text': request_data['text']})

    response_data = response.json()
    return jsonify(response_data)
