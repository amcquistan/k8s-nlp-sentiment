#!/bin/bash

PROFILE=$1

eksctl create cluster -f cluster.yaml --profile $PROFILE
