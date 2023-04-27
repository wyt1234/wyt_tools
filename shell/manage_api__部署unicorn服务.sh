#!/bin/bash

API_MODULE="api_server:app"
NUM_WORKERS=1
HOST="0.0.0.0"
PORT=5001
PID_FILE="gunicorn-uvicorn.pid"
LOG_FILE="gunicorn-uvicorn.log"
TIMEOUT=600
LOG_LEVEL="debug"

start() {
    echo "Starting gunicorn-uvicorn server..."
    gunicorn -k uvicorn.workers.UvicornWorker --workers $NUM_WORKERS --bind $HOST:$PORT --timeout $TIMEOUT --pid $PID_FILE --log-file $LOG_FILE --log-level $LOG_LEVEL $API_MODULE &
    echo "Server started."
}

stop() {
    echo "Stopping gunicorn-uvicorn server..."
    if [ -f $PID_FILE ]; then
        kill -TERM `cat $PID_FILE`
        rm $PID_FILE
        echo "Server stopped."
    else
        echo "No gunicorn-uvicorn server running."
    fi
}

restart() {
    stop
    sleep 3
    start
}

usage() {
    echo "Usage: ./manage_api.sh {start|stop|restart}"
}

if [ $# -ne 1 ]; then
    usage
else
    case $1 in
        "start")
            start
            ;;
        "stop")
            stop
            ;;
        "restart")
            restart
            ;;
        *)
            usage
            ;;
    esac
fi
