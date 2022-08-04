#!/usr/bin/env bash
docker stop graylog-xw
docker rm graylog-xw

docker run \
--link graylog_mongo:mongo \
--link graylog_es:docker.elastic.co/elasticsearch/elasticsearch \
--name graylog-xw \
-p 9000:9000 \
-p 12201:12201/udp \
-v /home/aminer/deploy/graylog.conf:/usr/share/graylog/data/config/graylog.conf \
-e GRAYLOG_PASSWORD_SECRET="somepasswordpepper" \
-e GRAYLOG_ROOT_USERNAME="admin" \
-e GRAYLOG_ROOT_PASSWORD_SHA2="8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918" \
-e GRAYLOG_HTTP_EXTERNAL_URI="http://192.168.0.29:9000/" \
-e GRAYLOG_WEB_ENDPOINT_URI="http://192.168.0.29:9000/:9000/api" \
-e GRAYLOG_ELASTICSEARCH_HOSTS="http://192.168.0.29:9200" \
-e GRAYLOG_MONGODB_URI="mongodb://192.168.0.29:2707/graylog" \
-e GRAYLOG_ROOT_TIMEZONE="Asia/Shanghai"  \
-d graylog/graylog:3.1


