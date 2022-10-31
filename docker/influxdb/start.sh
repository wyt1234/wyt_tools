docker run \
    --name influxdb \
    -p 8086:8086 \
      --volume /data/influxdb:/var/lib/influxdb2 \
    influxdb:2.4.0