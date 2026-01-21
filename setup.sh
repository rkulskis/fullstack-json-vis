#!/bin/bash

DATASET_URL="${1:-https://static.krevera.com/dataset.json}"

# Get data, spoofing user agent to bypass normal curl blocker
curl -A "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0" \
     "${DATASET_URL}" > dataset.json

docker run --name postgres \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=db \
  -p 5432:5432 \
  -d postgres:16
