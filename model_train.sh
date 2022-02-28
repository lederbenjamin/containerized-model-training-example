#!/bin/bash

docker build -t ml_app .
container_id=$(docker run -dp 3000:3000 ml_app)
while ! docker exec "$container_id" /is_ready.sh; do sleep 1; done
mkdir -p models
current_time=$(date "+%Y.%m.%d-%H.%M.%S")
docker cp "$container_id":text_classifier.tar.gz models/text_classifier_"$current_time".tar.gz
docker stop "$container_id"