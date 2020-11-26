#!/usr/bin/env bash
cd $(cd -P -- "$(dirname -- "$0")" && pwd -P)
docker-compose build
docker-compose push || true
docker stack deploy --compose-file docker-compose.yml add-datastore
