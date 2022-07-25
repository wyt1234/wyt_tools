#!/usr/bin/env bash

docker stop mongodb
docker rm mongodb

docker run -d -p 27017:27017 \
--restart=always \
--log-opt max-size=100m --log-opt max-file=3 \
-v /home/aminer/data/mongo:/data/db \
--name mongodb \
mongo:3.6.22 --auth