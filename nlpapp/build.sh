#!/bin/bash

VERSION=$1

docker build --tag flask-nlp-app:$VERSION .
docker tag flask-nlp-app:$VERSION adammcquistan/flask-nlp-app:$VERSION

