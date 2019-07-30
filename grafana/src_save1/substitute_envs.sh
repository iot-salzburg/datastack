#!/bin/bash -e
export DBINDEX="[nimble-]YYYY.MM"

cd $(cd -P -- "$(dirname -- "$0")" && pwd -P)
envsubst < datasource_template.yml > provisioning/datasources/all.yml
