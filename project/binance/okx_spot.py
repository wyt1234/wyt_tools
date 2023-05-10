import time

import okx.Trade as Trade

import okx.Funding as Funding
import okx.Convert as Convert
from okx.MarketData import MarketAPI

import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 获取配置文件中的数据
api_key = config.get('OKX', 'api_key')
secret_key = config.get('OKX', 'secret_key')
passphrase = config.get('OKX', 'passphrase')

flag = "0"  # live trading: 0, demo trading: 1
convertAPI = Convert.ConvertAPI(api_key, secret_key, passphrase, False, flag)
marketAPI = MarketAPI(api_key, secret_key, passphrase, False, flag)


# (行情)获取单个产品行情信息
def market_ticker(instId='BTC-USDT-SWAP'):
    # result = marketAPI.get_ticker(instId='BTC-USD-SWAP')
    # print(result)
    result = marketAPI.get_ticker(instId)
    print(result)
    return result


# 获取闪兑币种列表(欧易有300+种)
def get_currencies():
    result = convertAPI.get_currencies()
    print(result)
    ccys = [x['ccy'] for x in result['data']]
    return ccys


# （闪兑）预估询价 +USDT方向 -> xxx-USDT
def estimate_quote_sell(baseCcy='BTC', quoteCcy='USDT', side='sell', rfqSz=1, rfqSzCcy='BTC'):
    # baseCcy = "BTC"
    # quoteCcy = "USDT"
    # side = "sell"
    # rfqSz = "1"
    # rfqSzCcy = "BTC"
    result = convertAPI.estimate_quote(baseCcy, quoteCcy, side, rfqSz, rfqSzCcy)
    print(result)
    print(f"：{result['data'][0]['cnvtPx']}")
    return result


# （闪兑）反USDT方向 -> USDT-xxx
def estimate_quote_buy(baseCcy='BTC', quoteCcy='USDT', side='buy', rfqSz=100, rfqSzCcy='USDT'):
    # baseCcy = "BTC"
    # quoteCcy = "USDT"
    # side = "buy"
    # rfqSz = "100"
    # rfqSzCcy = "USDT"
    result = convertAPI.estimate_quote(baseCcy, quoteCcy, side, rfqSz, rfqSzCcy)
    print(result)
    print(f"：{result['data'][0]['cnvtPx']}")
    return result


if __name__ == '__main__':
    get_currencies()
    # estimate_quote_sell()
    # estimate_quote_buy()
    # market_ticker()

    # for i in range(30):
    #     estimate_quote_sell()
    #     # market_ticker()
    #     time.sleep(1)
