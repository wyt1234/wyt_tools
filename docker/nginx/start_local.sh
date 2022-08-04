#!/usr/bin/env bash

# mac m1 本地测试
docker stop test-nginx
docker rm test-nginx

docker run -d -p 80:80 \
--name=test-nginx \
-v /Users/xuwei/shenzhen_aminer/shenzhen_deploy/nginx/nginx_local.conf:/etc/nginx/nginx.conf  \
-v /Users/xuwei/shenzhen_aminer/covid_group/covid19/build:/usr/share/nginx/test_html \
arm64v8/nginx:1.20
