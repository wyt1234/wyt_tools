#!/usr/bin/env bash
docker stop logstash-elk
docker rm logstash-elk
docker run -d --name=logstash-elk \
--restart=always \
-v /home/xuwei/elk/conf/monitor.conf:/usr/share/logstash/monitor.conf \
122.200.68.33:5000/logstash_slave2:v6.5.5 bin/logstash -f monitor.conf
