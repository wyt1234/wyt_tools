#!/usr/bin/env bash

docker stop kibana-elk
docker rm kibana-elk

docker run -d -p 5601:5601 \
--name kibana-elk \
--restart=always \
--link es-elk:elasticsearch \
-e ELASTICSEARCH_URL="http://elasticsearch:9200" \
-e ELASTICSEARCH_USERNAME="admin" \
-e ELASTICSEARCH_PASSWORD="admin@2022" \
-e XPACK_MONITORING_ENABLED="false" \
-e XPACK_SECURITY_SECURECOOKIES="true" \
-e I18N_LOCALE=zh-CN \
kibana:7.3.2

#-v yml:/usr/share/kibana/config/kibana.yml