#!/bin/bash

url="https://braindev.itic-sci.com/sci_brain/rec-sys/chat/completions"
authorization="Bearer token1"

# 要模拟的并发用户数量
concurrency=10

# 要执行的总请求数量
total_requests=10

# 记录开始时间
start_time=$(date +%s)

# 使用 seq 和 xargs 并行发送请求
seq "$total_requests" | xargs -P "$concurrency" -I{} curl -s -N --location "$url" \
    --header 'Content-Type: application/json' \
    --header "Authorization: $authorization" \
    --header 'Origin: http://localhost:8000' \
    --data '{
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "你好!"}],
            "stream": true,
            "max_tokens": 2048
        }' >/dev/null 2>&1

# 记录结束时间
end_time=$(date +%s)

# 计算并输出执行时间
duration=$((end_time - start_time))
echo "Completed $total_requests requests in $duration seconds"
