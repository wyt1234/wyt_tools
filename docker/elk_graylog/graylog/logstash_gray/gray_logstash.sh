#!/usr/bin/env bash
docker pull 122.200.68.33:5000/gray_logstash:v1

docker stop logstash-graylog
docker rm logstash-graylog

docker run -d --name=logstash-graylog \
-v /Users/xuwei/my_project/selfclass/graylog/logstash_gray/gray_logstash.conf:/usr/share/logstash/gray_logstash.conf \
122.200.68.33:5000/gray_logstash:v1 bin/logstash -f gray_logstash.conf
