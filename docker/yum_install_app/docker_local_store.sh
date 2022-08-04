#!/bin/bash

# Nexus 从 3.0 版本也开始支持创建 Docker 镜像仓库了
# -e INSTALL4J_ADD_VM_PARAMS="-Xms4g -Xmx4g -XX:MaxDirectMemorySize=8g" \ # 如果不需要限制 java 内存请删除此行

###
# 映射端口对应的用途：
#8081：可以通过http访问nexus应用
#8082：docker(hosted)私有仓库，可以pull和push
#8083：docker(proxy)代理远程仓库，只能pull
#8084：docker(group)私有仓库和代理的组，只能pull
#使用参数 -v 建立宿主机与Docker目录映射关系，/nexus-data：docker里存nexus数据目录，所以将数据目录存放到宿主机/root/data/nexus

# chown -R 200 /root/data/nexus

# admin/aminer@2022

# docker pull 192.168.0.28:8082/images:v1

docker stop nexus3
docker rm nexus3

docker run -dti --name nexus3 \
--restart=always \
-p 8081:8081 -p 8082:8082 -p 8083:8083 -p 8084:8084 \
-e INSTALL4J_ADD_VM_PARAMS="-Xms4g -Xmx4g -XX:MaxDirectMemorySize=8g" \
-v /etc/localtime:/etc/localtime \
-v /root/data/nexus:/nexus-data \
sonatype/nexus3:3.38.1
