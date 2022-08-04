#!/bin/bash

docker build . -t  122.200.68.33:5000/gray_logstash:v1

docker push  122.200.68.33:5000/gray_logstash:v1