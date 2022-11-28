echo "current PID: $$" #这句删除也可以
cd /home/wyt/project
nohup jupyter-lab --port 39001 --allow-root --ip=0.0.0.0 >/home/wyt/project/wyt_tools/deploy/deploy_jupyterlab/jupyterlab.log 2>&1 &
echo "$!"
echo "$!" >/home/wyt/project/wyt_tools/deploy/deploy_jupyterlab/pid #将上一个后台进程写入到pid文件中
