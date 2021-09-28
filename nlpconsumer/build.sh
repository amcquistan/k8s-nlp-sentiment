#!/bin/bash

VERSION=$1

docker build --tag nlp-kafka-consumer:$VERSION .
docker tag nlp-kafka-consumer:$VERSION adammcquistan/nlp-kafka-consumer:$VERSION

