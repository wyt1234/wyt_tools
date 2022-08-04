#!/bin/bash

# 安装docker，并和28服务器上的docker私有仓库建立连接，之后
# docker push 192.168.0.28:8082/images:v1
# docker pull 192.168.0.28:8082/images:v1

sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine

sudo yum remove docker-ce docker-ce-cli containerd.io
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd


sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
sudo yum makecache fast
sudo yum -y install docker-ce-18.06.1.ce-3.el7

# 加入国内镜像源
sudo mkdir -p /etc/docker
# 使用28服务器搭建的docker私服
# Docker默认存储位置 "graph": "/home/docker"
sudo echo -e  "{\"insecure-registries\": [\"192.168.0.28:8082\",\"192.168.0.28:8084\"], \"registry-mirrors\": [\"https://hub-mirror.c.163.com\",\"https://mirror.baidubce.com\"], \"graph\": \"/home/docker\"}" > /etc/docker/daemon.json
#sudo echo -e  "{\"registry-mirrors\": [\"https://hub-mirror.c.163.com\",\"https://mirror.baidubce.com\"]}" > /etc/docker/daemon.json

# 启动docker
sudo systemctl start docker

# 设置开机启动
sudo systemctl enable docker
sudo systemctl daemon-reload
sudo systemctl restart docker

# admin/aminer@2022
sudo docker login 192.168.0.28:8082