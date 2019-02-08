#!/usr/bin/env bash
echo "Printing 'docker service ls | grep add-datastore':"
docker service ls | grep add-datastore
echo ""
echo "Printing 'docker stack ps add-datastore':"
docker stack ps add-datastore
