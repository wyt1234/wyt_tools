#!/usr/bin/env bash

docker stop gitlab

docker rm gitlab

docker run -d --restart=always \
--hostname gitlab --name=gitlab \
-p 1443:443 -p 2002:2002 -p 122:22 \
-v /etc/localtime:/etc/localtime \
-v /home/aminer/shenzhen_deploy/git/gitlab.rb:/etc/gitlab/gitlab.rb \
-v /home/data/gitlab/config:/etc/gitlab \
-v /home/data/gitlab/logs:/var/log/gitlab \
-v /home/data/gitlab/data:/var/opt/gitlab \
--shm-size 520m \
gitlab/gitlab-ce:14.9.3-ce.0



