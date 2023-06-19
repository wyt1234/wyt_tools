#!/bin/bash

url="https://braindev.itic-sci.com/sci_brain/rec-sys/chat/completions"
authorization="Bearer token1"

# 输出开始信息
echo "Starting script..."

# 初始化一个变量来存储开始时间和收到的第一个响应
start_time=$(echo "$(date +%s) * 1000 + $(date +%3N)" | bc)
first_response_received=false

# 使用 curl 监听 EventStream 并用 while 循环处理每一条消息
curl -s -N --location "$url" \
  --header 'Content-Type: application/json' \
  --header "Authorization: $authorization" \
  --header 'Origin: http://localhost:8000' \
  --data '{
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "你好!"}],
        "stream": true,
        "max_tokens": 2048
    }' 2>>error.log | while read -r line; do
  # 输出接收到的行
  echo "Received line: $line"

  # 检查行是否以"data:"开始
  if [[ $line == data:* ]]; then
    current_time=$(echo "$(date +%s) * 1000 + $(date +%3N)" | bc)
    time_since_start=$(echo "$current_time - $start_time" | bc)

    # 检查是否是第一个响应
    if [ "$first_response_received" = false ]; then
      first_response_received=true
      echo "Time to first response: $time_since_start ms"
    else
      echo "Time since start: $time_since_start ms"
    fi

    # 记录事件和时间
    event_data=${line#data: }
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] Received event: $event_data" >>events.log

    # 检查是否是结束消息
    if [[ $event_data == " [DONE]" ]]; then
      echo "Stream completed. Exiting."
      break
    fi
  fi

done

# 输出结束信息
echo "Script completed."
