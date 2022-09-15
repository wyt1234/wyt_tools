#!/bin/bash

SSH_USER="root"
SSH_PSWD="aminer@2022"
SSH_PROT="22"

CHECK_DATE=`date "+%Y_%m_%d_%H_%M_%S"`
cp base_check.sh ${CHECK_DATE}_base_check.sh
TMP_FILE=${CHECK_DATE}_base_check.sh
# create log file
mkdir ./check_log_${CHECK_DATE}
touch ./check_log_${CHECK_DATE}/${TMP_FILE}.log
LOG_FILE=./check_log_${CHECK_DATE}/${TMP_FILE}.log
SSH_IP=`egrep -o "^(\b([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\b\.){3}\b([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\b" env_conf.ini`
# ip 可以从其他文件获取，也可以直接放在这以数组的形式就行，或者以空格分开直接放在这。
CHECK_SCRIPT="/tmp/${TMP_FILE}"
scp_exec(){
expect << EOF
	set timeout -1
	spawn scp -r ${TMP_FILE} ${SSH_USER}@${i}:/tmp
	expect {
	    "password" {send "${SSH_PSWD}\r";}
	    "yes/no" {send "yes\r";exp_continue}
	}
	expect eof
EOF
}
ssh_exec(){
expect << EOF
        set timeout 10
        spawn ssh -p ${SSH_PROT} ${SSH_USER}@${i}
        expect {
                "yes/no" {send "yes\r"; exp_continue}
                "password" {send "${SSH_PSWD}\r"}
        }
        expect -re ".*\[\$#\]"
        send -- "bash ${CHECK_SCRIPT}\r"
        expect -re ".*\[\$#\]"
		    # send -- "rm -rf ${CHECK_SCRIPT}\r"
        expect -re ".*\[\$#\]"
        send "exit\r"
        expect eof
EOF
}
total_num=0
for i in ${SSH_IP}
do
  echo "正在执行：${i}"
	scp_exec >> ${LOG_FILE} 2>&1
	ssh_exec >> ${LOG_FILE} 2>&1
  total_num=`expr $total_num + 1`
	success_num=`grep -o '64 bytes from 192.168.0.254' ${LOG_FILE}  |wc -l`
	echo "成功数/总数：${success_num}/${total_num}"
done
rm -rf ${TMP_FILE}
echo "complete!"
