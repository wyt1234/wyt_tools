import time

import okx.Trade as Trade

import okx.Funding as Funding
import okx.Convert as Convert

import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 获取配置文件中的数据
api_key = config.get('OKX', 'api_key')
secret_key = config.get('OKX', 'secret_key')
passphrase = config.get('OKX', 'passphrase')

flag = "1"  # live trading: 0, demo trading: 1
convertAPI = Convert.ConvertAPI(api_key, secret_key, passphrase, False, flag)


# 获取闪兑币种列表（测试网络）
def get_currencies():
    result = convertAPI.get_currencies()
    print(result)


# 闪兑预估询价
def estimate_quote():
    baseCcy = "BTC"
    quoteCcy = "USDT"
    side = "sell"
    rfqSz = "0.01"
    rfqSzCcy = "BTC"
    result = convertAPI.estimate_quote(baseCcy, quoteCcy, side, rfqSz, rfqSzCcy)
    # print(result)
    print(f"：{result['data'][0]['cnvtPx']}")


if __name__ == '__main__':
    # get_currencies()
    for i in range(30):
        estimate_quote()
        time.sleep(1)
