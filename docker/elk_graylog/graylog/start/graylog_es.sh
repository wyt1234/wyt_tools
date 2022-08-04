#!/usr/bin/env bash
docker stop graylog_es
docker rm graylog_es

docker run \
--name graylog_es \
-p 9200:9200 -p 9300:9300 \
-v /home/aminer/data/es/data:/usr/share/elasticsearch/data \
-e "discovery.type=single-node" \
-e http.cors.allow-origin="*" \
-e http.cors.enabled=true \
-d docker.elastic.co/elasticsearch/elasticsearch:6.3.2



docker run \
--name graylog_es \
-p 9400:9200 -p 9500:9300 \
-e "discovery.type=single-node" \
-e http.cors.allow-origin="*" \
-e http.cors.enabled=true \
-d docker.elastic.co/elasticsearch/elasticsearch:6.3.2