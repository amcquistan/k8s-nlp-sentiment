# Architecture Guild Presentation

Notes and outline of steps to demonstrate building and deploying containerized NLP app to K8s

## A) Simplified Sentiment REST API Microservice

In this section I introduce the basics of the TextBlob NLP library for calculating sentiment,
including how to wrap the TextBlob NLP library in Flask REST API, containerize it and deploy it
to a Kubernetes (K8s) cluster.

### Build Sentiment API Locally

Create sentiment service api directory structure.

```
mkdir -p sentimentapi/sentimentapi
cd sentimentapi
```

Create requirements.txt

```
flask>=2.0.1,<2.1.0
gunicorn>=20.1.0,<20.2.0
textblob>=0.15.3,<0.16.0
```

Create virtual env and install dependencies.

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Download the NLP dictionaries and models.

```
python -m textblob.download_corpora
```

Build basic logic of REST API inside sentimentapi/sentimentapi/api.py

```
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

```

Launch sentiment api and test locally.

```
export FLASK_APP=sentimentapi.api
flask run
```

Test the REST API.

```
http POST http://localhost:5000/sentiment text="Coding is an amazing and fun activity."
```


### Containerize Sentiment API

Add a Docker file to sentimentapi

```
FROM python:3.8-slim-buster

COPY requirements.txt /

RUN pip3 install -r /requirements.txt

ENV NLTK_DATA=/app
RUN python -m textblob.download_corpora

COPY sentimentapi/ /app
WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["gunicorn", "api:app", "--threads", "5", "-b", "0.0.0.0:8000"]
```

Build image and push container to DockerHub.

```
VERSION=0.0.1
docker build --tag textblob-sentiment-api:$VERSION .
docker tag textblob-sentiment-api:$VERSION adammcquistan/textblob-sentiment-api:$VERSION
docker push adammcquistan/textblob-sentiment-api:$VERSION
```

Test locally with the container.

In one terminal.

```
docker run -p 8000:8000 textblob-sentiment-api:0.0.1
```

In second terminal.

```
http POST http://localhost:8000/sentiment text="Coding is an amazing and fun activity."
```

### Deploying Sentiment API to Kubernetes

Create a deployment of the textblob-sentiment-api:0.0.1 pod with two replicas.

```
kubectl create namespace simple-demo
kubectl create deployment sentiment-api \
  --replicas 2 \
  --image adammcquistan/textblob-sentiment-api:0.0.1 \
  --dry-run=client \
  --output yaml > deployment.yaml
```

Review and execute deployment.yaml

```
kubectl apply -f deployment.yaml --namespace simple-demo
```

Expose deployment with ClusterIP Service.

```
kubectl expose deployment sentiment-api \
    --port 80 \
    --target-port 8000 \
    --namespace simple-demo \
    --dry-run=client --output yaml > service.yaml
```


Review and execute service.yaml

```
kubectl apply -f service.yaml
```

Create a basic python3.8 pod in simple-demo namespace and test sentiment api on kubernetes.

```
kubectl run sentiment-tester \
    --image python \
    --restart Never \
    --namespace simple-demo \
    --command -- sleep infinity
```

Launch shell inside sentiment-tester pod, install httpie, test sentiment api.

```
kubectl exec -it sentiment-tester --namespace simple-demo -- sh
pip install httpie
http POST http://sentiment-api/sentiment text="Coding is an amazing and fun activity."
```


## B) Expanded NLP App

In this section I expand on the simple sentiment REST API microservice by:

* add Kafka message queue to K8s cluster
* implement NLP calculations as a Kafka consumer application
* update the sourcing of input text to come from a web page scraped from the internet
* add noun phrase extraction to the NLP calculations
* add a simple flask based frontend for collecting a web page url
* add a REST API endpoint to receive the web url and publish to kafka topic
* add redis to save results 

See regular [README.md](README.md) for additional notes.
