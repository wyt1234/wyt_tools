#!/usr/bin/env bash

docker stop redis
docker rm redis

docker run -p 6379:6379 --name redis \
--log-opt max-size=100m --log-opt max-file=3 \
-m 20G \
-v /home/data/redis:/data \
-d redis:6.2.6 \
redis-server --appendonly yes \
--requirepass "aminer@2022"
