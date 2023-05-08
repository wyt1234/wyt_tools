#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from binance.spot import Spot
from binance.lib.utils import config_logging
from datetime import datetime
import time
import configparser

'''测试网'''


# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 获取配置文件中的数据
api_key = config.get('BINANCE', 'api_key')
api_secret = config.get('BINANCE', 'api_secret')


spot_client = Spot(api_key, api_secret, testnet=True)


def getQuote():
    # 设置要转换的资产和金额
    from_asset = 'BTC'
    to_asset = 'USDT'
    from_amount = 0.1
    to_amount = None
    # 发送获取报价请求
    response = spot_client.sapi_post('/sapi/v1/convert/getQuote', params={
        'fromAsset': from_asset,
        'toAsset': to_asset,
        'fromAmount': from_amount,
        'toAmount': to_amount,
        'walletType': 'SPOT',
        'validTime': '10s',
        'timestamp': int(time.time() * 1000)
    })
    # 打印获取报价请求的响应
    print(response)


if __name__ == '__main__':
    getQuote()
