#!/usr/bin/env bash
echo "Printing 'docker service ls | grep stack':"
docker service ls | grep stack
echo ""
echo "Printing 'docker stack ps stack':"
docker stack ps stack
