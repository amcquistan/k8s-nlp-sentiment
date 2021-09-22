#!/bin/bash

VERSION=$1

docker build --tag textblob-sentiment-app:$VERSION .
docker tag textblob-sentiment-app:$VERSION adammcquistan/textblob-sentiment-app:$VERSION

