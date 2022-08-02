#!/bin/bash

# scrapyd 启动，停止，重启scrapyd服务

notes='
启动服务：bash run_jupyterlab_server.sh start
停止服务：bash run_jupyterlab_server.sh stop
重启服务：bash run_jupyterlab_server.sh restart
实时日志：bash run_jupyterlab_server.sh tail
'

action=$1

function star_server() {
  echo "current PID: $$" #这句删除也可以
  cd /home/wyt/project
  nohup jupyter-lab --port 39001 --allow-root --ip=0.0.0.0 >/home/wyt/project/wyt_tools/deploy/deploy_jupyterlab/jupyterlab.log 2>&1 &
  echo "$!"
  echo "$!" >/home/wyt/project/wyt_tools/deploy/deploy_jupyterlab/pid #将上一个后台进程写入到pid文件中
  cd /home/wyt/project/wyt_tools/deploy/deploy_jupyterlab
}

function stop_server() {
  kill $(cat pid)
}

function restart_server() {
  stop_server
  sleep 2
  star_server
}

if [ -z "$action" ]; then
  echo "${notes}"
  echo "Error: action param is not null"

elif [ $action = "-h" ] || [ $action = "--help" ] || [ $action = "h" ]; then
  echo "${notes}"
  echo "确保启用了conda环境"
elif [ "$action" = "start" ]; then
  star_server
elif [ "$action" = "stop" ]; then
  stop_server
elif [ "$action" = "restart" ]; then
  restart_server
else
  echo "Error: param error"
fi
