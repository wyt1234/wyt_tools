###指定配置文件挂载路径/data/brain_mysql/conf/my.cnf

docker stop brain_mysql
docker rm brain_mysql

docker run -p 3306:3306 --name brain_mysql \
--restart=always \
--log-opt max-size=100m --log-opt max-file=3 \
-v /home/aminer/data/mysql:/var/lib/mysql \
-v /home/aminer/data/mysql-files:/var/lib/mysql-files \
-v /home/aminer/data/conf/mysqld.cnf:/etc/mysql/my.cnf \
-e TZ="Asia/Shanghai" \
-e MYSQL_ROOT_PASSWORD=brain@2022 \
-d mysql:8.0.15 \
--default-authentication-plugin=mysql_native_password


