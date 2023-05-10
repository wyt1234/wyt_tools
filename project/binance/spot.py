# 接口类
import time


class SPOT:
    def __int__(self):
        self.quotes = []
        self.alive = []

    def trade_buy_side(self):
        return

    def trade_sell_side(self):
        return

    def fetch_flash_swap_buy_side(self):
        return

    def fetch_flash_swap_sell_side(self):
        return

    def fetch_ticker(self):
        return

    def refresh_balance(self):
        return

    def _clear_timeout(self):
        return


class QUOTE:
    def __int__(self):
        self.quoteId = ''
        self.fromAsset = ''
        self.toAsset = ''
        self.toAmount = ''
        self.createTime = ''
        self.endTime = int(time.time() * 1000)
        self.ttlMs = ''

    def _update_endtime(self):
        self.endTime = self.createTime + self.ttlMs

    def is_valid(self):
        return self.endTime > int(time.time() * 1000)

