docker stop brain_es
docker rm brain_es

docker run --name brain_es \
--restart=always \
-d -p 9200:9200 -p 9300:9300 \
--log-opt max-size=100m --log-opt max-file=3 \
-v /home/aminer/data/es:/usr/share/elasticsearch/data \
-e "discovery.type=single-node" \
-e "xpack.security.enabled=false" \
es_security:v1
