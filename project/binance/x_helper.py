import configparser
import os
import threading
import time
from typing import List
from loguru import logger
from prettytable import PrettyTable
from prometheus_client import Gauge, start_http_server
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from base import BASE_QUOTE, TICK

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')
influx_host = config.get('influx', 'host')
influx_token = config.get('influx', 'token')
influx_org = config.get('influx', 'org')


# 使用influxDB记录
def update_influxdb(HISTORY: List[BASE_QUOTE]):
    client = InfluxDBClient(url=f"http://{influx_host}:8086", token=f"{influx_token}", org=f"{influx_org}")
    write_api = client.write_api(write_options=SYNCHRONOUS)
    query_api = client.query_api()
    bucket = "flash_swap"
    while True:
        # 查询 InfluxDB 中最新的时间戳
        query = f'from(bucket: "{bucket}") |> range(start: -1d) |> last()'
        result = query_api.query(query)
        latest_timestamp = None
        if result:
            for table in result:
                for record in table.records:
                    latest_timestamp = record.get_time().timestamp() * 1000  # 纳秒转换为秒
        points = []
        for item in HISTORY:
            # 空，跳过
            if not item:
                continue
            # 只处理比最新时间戳更新的数据
            if latest_timestamp is None or item.createTime > latest_timestamp:
                # tick
                if isinstance(item, TICK):
                    point = Point("tick") \
                        .tag("pair", f"{item.fromAsset}_{item.toAsset}") \
                        .tag("market_name", item.market_name) \
                        .field("last", float(item.last)) \
                        .field("lastSz", float(item.lastSz)) \
                        .field("createTime", int(item.createTime)) \
                        .time(int(item.createTime) * 1000000)  # InfluxDB 需要纳秒级时间戳
                # flash_swap
                else:
                    point = Point("flash_swap_data") \
                        .tag("pair", f"{item.fromAsset}_{item.toAsset}") \
                        .tag("side", item.side) \
                        .tag("market_name", item.market_name) \
                        .field("fromAmount", float(item.fromAmount)) \
                        .field("toAmount", float(item.toAmount)) \
                        .field("cnvtPx", float(item.cnvtPx)) \
                        .field("quoteSz", float(item.quoteSz)) \
                        .field("createTime", int(item.createTime)) \
                        .field("endTime", int(item.endTime)) \
                        .field("ttlMs", int(item.ttlMs)) \
                        .time(int(item.createTime) * 1000000)  # InfluxDB 需要纳秒级时间戳
                points.append(point)
        if points:
            write_api.write(bucket, record=points)
            logger.info(f"Wrote {len(points)} points to InfluxDB")
        else:
            logger.info("No new points to write to InfluxDB")
            time.sleep(0.3)
        time.sleep(0.3)  # 每1秒写入一次数据到 InfluxDB


# 控制台监控
def monitor_alive_and_history(ALIVE, HISTORY):
    def print_table(alive_count, history_count):
        table = PrettyTable()
        table.field_names = ["Metrics", "Count"]
        table.add_row(["ALIVE", alive_count])
        table.add_row(["HISTORY", history_count])
        print(table)

    def clear_console():
        if os.name == 'posix':  # Unix/Linux/MacOS/BSD
            os.system('clear')
        elif os.name == 'nt':  # Windows
            os.system('cls')

    clear_interval = 3600  # 清理间隔（以秒为单位）
    counter = 0
    while True:
        # 执行ALIVE清理
        ALIVE.remove_dead_quotes()
        alive_count = len(ALIVE.live_quotes)
        history_count = len(HISTORY)
        # clear_console()
        print_table(alive_count, history_count)
        counter += 1
        if counter >= clear_interval:
            with threading.Lock():  # 为了线程安全，使用锁来清空列表
                HISTORY.clear()
                print("HISTORY cleared.")
            counter = 0
        time.sleep(2)


# 创建一个 Prometheus Gauge，用于保存 HISTORY 中的数据
history_gauge = Gauge("history", "The history of the market data", ["pair", "side"])


# 推送到prometheus
def update_prometheus(HISTORY: List[BASE_QUOTE]):
    while True:
        for item in HISTORY:
            pair = f"{item.fromAsset}_{item.toAsset}"
            side = item.side
            value = float(item.cnvtPx)
            history_gauge.labels(pair=pair, side=side).set(value)
        time.sleep(5)  # 每5秒更新一次 Prometheus Gauge
