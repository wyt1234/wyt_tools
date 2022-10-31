#https://docs.influxdata.com/influxdb/v2.4/install/?t=Docker#persist-data-outside-the-influxdb-container

docker run \
  --name influxdb \
  -p 8086:8086 \
  --volume /data/influxdb:/var/lib/influxdb2 \
  influxdb:2.4.0
