# 部署节点 192.168.0.3
#cp conf/* /home/aminer/clickhouse/conf/
docker run -d --name=clickhouse-server \
  -p 8123:8123 -p 9009:9009 -p 9000:9000 \
  --ulimit nofile=262144:262144 \
  -v /home/aminer/clickhouse/conf/config.xml:/etc/clickhouse-server/config.xml \
  -v /home/aminer/clickhouse/conf/users.xml:/etc/clickhouse-server/users.xml \
  -v /home/aminer/clickhouse/log:/var/log/clickhouse-server \
  -v /home/aminer/clickhouse/clickhouse_database:/var/lib/clickhouse \
  yandex/clickhouse-server
