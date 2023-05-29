import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
# 获取配置文件中的数据
api_key = config.get('LiveCoinWatch', 'api_key')
influx_host = config.get('influx', 'host')
influx_token = config.get('influx', 'token')
influx_org = config.get('influx', 'org')
buckets = 'livecoinwatch'


def coin_list():
    url = "https://api.livecoinwatch.com/coins/list"
    payload = json.dumps({
        "currency": "USD",
        "sort": "rank",
        "order": "ascending",
        "offset": 0,
        "limit": 2,
        "meta": True
    })
    headers = {
        'content-type': 'application/json',
        'x-api-key': api_key
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())


def run():
    coin_list()
    return


if __name__ == '__main__':
    run()
