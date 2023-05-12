# 接口类
import time
from typing import Dict


class BASE_QUOTE:
    def __init__(self):
        # 属性
        self.quoteId = ''
        self.fromAsset = ''
        self.toAsset = ''
        # 报价
        self.fromAmount = ''  # 来源数量
        self.toAmount = ''  # 目标数量
        self.cnvtPx = ''  # 兑换单价
        self.quoteSz = ''  # 实际兑换数量
        # 时间
        self.createTime = ''  # quoteTime
        self.endTime = int(time.time() * 1000)  # 截止时间
        self.ttlMs = 500  # 窗口长度
        # 筛选属性
        self.market_name = 'base_market'
        self.side = ''

    def _update_endtime(self):
        self.endTime = self.createTime + self.ttlMs

    # 是否存活
    def is_alive(self):
        return self.endTime > int(time.time() * 1000)


class BASE_SPOT:
    def __init__(self):
        self.market_name = 'base'
        self.history_quotes = []  # [BASE_QUOTE()]
        self.alive_quotes = []  # [BASE_QUOTE()]

    def get_currencies(self):
        return [('BTC', 'USDT')]

    # 获取闪兑报价（buy USDT方向：BTC -> USDT）
    def flash_swap_fetch_flash_swap_buy_side(self, fromAsset, toAsset, fromAmount) -> BASE_QUOTE:
        '''buy'''
        return BASE_QUOTE()

    # 获取闪兑报价（sell USDT方向：USDT -> BTC）
    def flash_swap_fetch_sell_side(self, fromAsset, toAsset, toAmount) -> BASE_QUOTE:
        return BASE_QUOTE()

    # 执行闪兑交易
    def flash_swap_execute_trade_buy_side(self, quotes_id):
        '''buy'''
        return

    # 执行闪兑交易
    def flash_swap_execute_trade_sell_side(self, quotes_id):
        '''sell'''
        return

    # 市价
    def fetch_ticker(self) -> Dict:
        return {'market_name': self.market_name, 'ts': 111111, 'last': 1}

    # 账户余额
    def account_refresh_balance(self):
        return

    # 清理报价
    def clear_quotes(self):
        return
