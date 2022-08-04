#!/usr/bin/env bash

docker stop techbrain_nginx
docker rm techbrain_nginx

docker run -d -p 80:80 -p 443:443 \
--name=techbrain_nginx \
-v /home/aminer/shenzhen_deploy/nginx/nginx_1.conf:/etc/nginx/nginx.conf \
-v /home/aminer/shenzhen_deploy/nginx/conf1.d:/etc/nginx/conf.d \
-v /home/aminer/logs/nginx:/var/log/nginx \
--restart=always \
-v /home/aminer/app:/usr/share/nginx/html \
-v /home/aminer/deepbc:/usr/share/nginx/deepbc \
-v /home/aminer/deepbc_api/static:/usr/share/nginx/static \
-v /home/aminer/home_recommend:/usr/share/nginx/home_recommend \
-v /home/aminer/covid19:/usr/share/nginx/covid19 \
-v /home/aminer/covid_dashboard:/usr/share/nginx/covid_dashboard \
-v /home/aminer/kj_graph/dist:/usr/share/nginx/kj_graph \
-v /home/aminer/aminer2c/dist:/usr/share/nginx/aminer2c \
nginx:1.20.1
