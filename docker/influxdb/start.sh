#https://docs.influxdata.com/influxdb/v2.4/install/?t=Docker#persist-data-outside-the-influxdb-container

docker run \
  --name influxdb \
  -p 8086:8086 \
  --restart=always \
  --volume /home/influxdb:/var/lib/influxdb2 \
  -d \
  influxdb:2.4.0

# generate the default configuration file
#docker run \
#  --rm influxdb:2.4.0 \
#  influxd print-config > /data/influxdb/config.yml