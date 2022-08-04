#!/usr/bin/env bash

docker stop aminer_shenzhen
docker rm aminer_shenzhen

docker run -d -p 80:80 \
--name=aminer_shenzhen \
-v /home/aminer/shenzhen_deploy/nginx/nginx2.conf:/etc/nginx/nginx.conf  \
-v /home/aminer/shenzhen_deploy/nginx/conf2.d:/etc/nginx/conf.d \
-v /home/aminer/logs/nginx:/var/log/nginx \
--restart=always \
-v /home/aminer/dist:/usr/share/nginx/html \
nginx:1.20.1
