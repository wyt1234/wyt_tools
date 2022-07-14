#!/bin/bash

declare -a usedTimes

# 不用idea格式化
function measure() {
    echo "command   : $@"
    usedTime="$( time ( `$@` ) 2>&1 1>/dev/null )"
    usedTimes+=("$usedTime")
    echo "time cost : $usedTime"
}

# 这里是需要计时的命令
measure echo ""

# 打印总耗时
echo ${usedTimes[*]}
