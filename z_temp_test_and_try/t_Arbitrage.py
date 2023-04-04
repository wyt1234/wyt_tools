import requests
import numpy as np


# 获取实时汇率
def get_exchange_rate(base_currency, target_currency, api_key):
    api_url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={base_currency}&to_currency={target_currency}&apikey={api_key}"
    response = requests.get(api_url)
    exchange_rate = float(response.json()['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    return exchange_rate


# 三角套利策略
def triangular_arbitrage(currency_a, currency_b, currency_c, api_key):
    # 获取实时汇率
    a_b_rate = get_exchange_rate(currency_a, currency_b, api_key)
    b_c_rate = get_exchange_rate(currency_b, currency_c, api_key)
    c_a_rate = get_exchange_rate(currency_c, currency_a, api_key)

    # 计算套利空间
    arbitrage_ratio = a_b_rate * b_c_rate * c_a_rate

    # 判断套利空间是否存在
    if arbitrage_ratio > 1.0:
        print(f"套利机会存在：{currency_a} -> {currency_b} -> {currency_c} -> {currency_a}")
    else:
        print("当前没有套利机会")


# 示例
api_key = "pBh4wZKyr0MqqJqu212FcmONpc0tdKW9"
currency_a = "USD"
currency_b = "EUR"
currency_c = "GBP"

triangular_arbitrage(currency_a, currency_b, currency_c, api_key)
