#!/bin/bash
# 设置 HTTP 和 HTTPS 代理
export HTTP_PROXY="http://127.0.0.1:4780"
export HTTPS_PROXY="http://127.0.0.1:4780"
echo "已设置 HTTP 代理为: $HTTP_PROXY"
echo "已设置 HTTPS 代理为: $HTTPS_PROXY"

# 获取当前脚本所在的目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# 定义脚本名称和日志文件路径
SCRIPT_NAME="x_gather_flash_swap.py"
LOG_FILE="$DIR/x_gather_flash_swap.log"
# 定义重启间隔（分钟）
RESTART_INTERVAL=1

# 定义一个函数来处理 SIGINT 信号
handle_sigint() {
    # 杀掉所有正在运行的脚本进程
    pkill -f $SCRIPT_NAME

    # 杀掉 sleep 进程
    kill $SLEEP_PID 2> /dev/null

    # 退出脚本
    exit
}

# 设置 trap 来捕获 SIGINT 信号
trap handle_sigint SIGINT

while true; do
    # 杀掉所有正在运行的脚本进程
    pkill -f $SCRIPT_NAME

    # 等待一段时间确保进程已经被成功杀掉
    sleep 5

    # 运行新的脚本进程，并直接在终端打印输出和写入日志
    echo "开始运行脚本：$SCRIPT_NAME"
    python3 $DIR/$SCRIPT_NAME | tee $LOG_FILE &

    # 获取 Python 进程的 PID
    PYTHON_PID=$!

    # 等待指定的分钟数
    sleep $(($RESTART_INTERVAL * 60)) &
    SLEEP_PID=$!

    # 设置一个 trap，在 sleep 完成后杀掉 Python 进程
    trap "kill $PYTHON_PID 2> /dev/null" 0

    # 等待 sleep 完成（这个会触发trap 0 信号）
    wait $SLEEP_PID

    # 移除 trap
    trap - 0
done
