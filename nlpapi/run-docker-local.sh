#!/bin/bash

# Running locally (without docker):
# gunicorn sentimentapi:app -b 0.0.0.0:8000

docker run -d -p 8000:8000 textblob-sentiment-api
