docker run -d --name=clickhouse-server \
  -p 8123:8123 -p 9009:9009 -p 9000:9000 \
  --ulimit nofile=262144:262144 \
  -v /Users/wyt/PJ/clickhouse_docker/conf/config.xml:/etc/clickhouse-server/config.xml \
  -v /Users/wyt/PJ/clickhouse_docker/conf/users.xml:/etc/clickhouse-server/users.xml \
  -v /Users/wyt/PJ/clickhouse_docker/log:/var/log/clickhouse-server \
  -v /Users/wyt/PJ/clickhouse_docker/clickhouse/clickhouse_database:/var/lib/clickhouse \
  yandex/clickhouse-server
