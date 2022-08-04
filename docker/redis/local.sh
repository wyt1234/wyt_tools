#!/usr/bin/env bash

docker stop redis
docker rm redis

#docker run -p 6379:6379 --name redis \
#--log-opt max-size=100m --log-opt max-file=3 \
#-d redis:6.2.6 \
#redis-server --appendonly yes


docker run -d --privileged=true -p 6379:6379 -v /Users/wyt/ARepo/shenzhen_deploy/db/redis/redis.conf:/etc/redis/redis.conf --name redis_local redis redis-server /etc/redis/redis.conf --appendonly yes