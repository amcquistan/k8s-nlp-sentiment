#!/bin/bash

VERSION=$1

docker build --tag textblob-sentiment-api:$VERSION .
docker tag textblob-sentiment-api:$VERSION adammcquistan/textblob-sentiment-api:$VERSION
