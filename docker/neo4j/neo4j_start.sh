#!/bin/bash

docker stop test-neo4j
docker rm test-neo4j

docker run --name test-neo4j  -p 7474:7474 -p 7687:7687  \
--restart=always \
--log-opt max-size=100m --log-opt max-file=3 \
-v /home/aminer/logs/neo4j_data:/data \
-d neo4j:4.4.3