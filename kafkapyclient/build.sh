#!/bin/bash

VERSION=$1

docker build --tag kafkapyclient:$VERSION .
docker tag kafkapyclient:$VERSION adammcquistan/kafkapyclient:$VERSION
