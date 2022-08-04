#!/usr/bin/env bash
docker stop graylog_mongo
docker rm graylog_mongo
docker run  \
--name graylog_mongo \
-p 2707:27017  \
-v /home/aminer/data/mongodb/configdb:/data/configdb/ \
-v /home/aminer/data/mongodb/db/:/data/db/ \
-d mongo:3.4
