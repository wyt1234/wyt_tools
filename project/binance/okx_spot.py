import time

import okx.Trade as Trade

import okx.Funding as Funding
import okx.Convert as Convert
from okx.MarketData import MarketAPI

import configparser

from base import BASE_SPOT, BASE_QUOTE


class OKX_SPOT(BASE_SPOT):

    def __init__(self):
        super().__init__()
        self.market_name = 'okx'
        # 读取配置文件
        config = configparser.ConfigParser()
        config.read('config.ini')
        # 获取配置文件中的数据
        api_key = config.get('OKX', 'api_key')
        secret_key = config.get('OKX', 'secret_key')
        passphrase = config.get('OKX', 'passphrase')
        flag = "0"  # live trading: 0, demo trading: 1
        self.convertAPI = Convert.ConvertAPI(api_key, secret_key, passphrase, False, flag)
        self.marketAPI = MarketAPI(api_key, secret_key, passphrase, False, flag)

    # (行情)获取单个产品行情信息
    # {'code': '0', 'msg': '', 'data': [{'instType': 'SWAP', 'instId': 'BTC-USDT-SWAP', 'last': '27712.7', 'lastSz': '30', 'askPx': '27712.8', 'askSz': '1363', 'bidPx': '27712.7', 'bidSz': '266', 'open24h': '27798', 'high24h': '27872', 'low24h': '27350', 'volCcy24h': '97715.74', 'vol24h': '9771574', 'ts': '1683721567699', 'sodUtc0': '27632.2', 'sodUtc8': '27401.5'}]}
    def market_ticker(self, instId='BTC-USDT-SWAP'):
        # result = marketAPI.get_ticker(instId='BTC-USD-SWAP')
        # print(result)
        result = self.marketAPI.get_ticker(instId)
        print(result)
        return result

    # 获取闪兑币种列表(欧易有300+种)
    def get_currencies(self):
        # result = self.convertAPI.get_currencies()
        # print(result)
        # ccys = [x['ccy'] for x in result['data']]
        # return ccys
        return [('BTC', 'USDT')]

    # （闪兑）预估询价 +USDT方向 -> xxx-USDT
    # {'code': '0', 'data': [{'baseCcy': 'BTC', 'baseSz': '1', 'clQReqId': '', 'cnvtPx': '26329.8372', 'origRfqSz': '1', 'quoteCcy': 'USDT', 'quoteId': 'quoterBTC-USDT16838855299743749', 'quoteSz': '26329.8372', 'quoteTime': '1683885529974', 'rfqSz': '1', 'rfqSzCcy': 'BTC', 'side': 'sell', 'ttlMs': '10000'}], 'msg': ''}
    def estimate_quote_buy(self, baseCcy='BTC', quoteCcy='USDT', side='sell', rfqSz=0.1, rfqSzCcy='BTC'):
        result = self.convertAPI.estimate_quote(baseCcy, quoteCcy, side, rfqSz, rfqSzCcy)
        print(result)
        print(f"：{result['data'][0]['cnvtPx']}")
        return result

    def flash_swap_fetch_flash_swap_buy_side(self, i, o, sz):
        result = self.estimate_quote_buy(i, o, 'sell', sz, i)['data'][0]
        quote = BASE_QUOTE()
        quote.quoteId = result['quoteId']
        quote.market_name = self.market_name
        quote.endTime = int(result['quoteTime']) + int(result['ttlMs'])
        quote.createTime = int(result['quoteTime'])
        quote.fromAsset = result['baseCcy']
        quote.toAsset = result['quoteCcy']
        quote.ttlMs = int(result['ttlMs'])
        quote.fromAmount = result['rfqSz']
        quote.toAmount = result['quoteSz']
        quote.cnvtPx = result['origRfqSz']
        quote.quoteSz = result['quoteSz']
        quote.side = 1
        self.alive_quotes.append(quote)
        return quote

    # （闪兑）反USDT方向 -> USDT-xxx
    # {'code': '0', 'data': [{'baseCcy': 'BTC', 'baseSz': '0.0037811222518307', 'clQReqId': '', 'cnvtPx': '26447.1745', 'origRfqSz': '100', 'quoteCcy': 'USDT', 'quoteId': 'quoter2BTC-USDT16838867761883194', 'quoteSz': '100', 'quoteTime': '1683886776188', 'rfqSz': '100', 'rfqSzCcy': 'USDT', 'side': 'buy', 'ttlMs': '10000'}], 'msg': ''}
    def estimate_quote_sell(self, baseCcy='BTC', quoteCcy='USDT', side='buy', rfqSz=100, rfqSzCcy='USDT'):
        result = self.convertAPI.estimate_quote(baseCcy, quoteCcy, side, rfqSz, rfqSzCcy)
        print(result)
        print(f"：{result['data'][0]['cnvtPx']}")
        return result

    def flash_swap_fetch_flash_swap_sell_side(self, i, o, sz):
        result = self.estimate_quote_sell(o, i, 'buy', sz, i)['data'][0]
        quote = BASE_QUOTE()
        quote.quoteId = result['quoteId']
        quote.market_name = self.market_name
        quote.endTime = int(result['quoteTime']) + int(result['ttlMs'])
        quote.createTime = int(result['quoteTime'])
        quote.fromAsset = result['quoteCcy']
        quote.toAsset = result['baseCcy']
        quote.ttlMs = int(result['ttlMs'])
        quote.fromAmount = result['origRfqSz']
        quote.toAmount = result['baseSz']
        quote.cnvtPx = result['cnvtPx']
        quote.quoteSz = result['quoteSz']
        quote.side = -1
        self.alive_quotes.append(quote)
        return quote


if __name__ == '__main__':
    c = OKX_SPOT()
    # c.get_currencies()
    # estimate_quote_sell()
    # c.estimate_quote_buy()
    c.flash_swap_fetch_flash_swap_buy_side('BTC', 'USDT', 0.1)
    c.flash_swap_fetch_flash_swap_sell_side('USDT', 'BTC', 100)
    # c.market_ticker()

    # for i in range(30):
    #     estimate_quote_sell()
    #     # market_ticker()
    #     time.sleep(1)
