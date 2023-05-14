import time

import okx_spot
from x_helper import monitor_alive_and_history, update_prometheus, update_influxdb
from thread_util import QuoteManager
import threading
from prettytable import PrettyTable
import os

'''
thread for collect data:
1、pull currencies 
2、check pair
3、ticker 
4、D/R 
5、(option)save bidirectional-transaction-def to alive
----
thread for trade（option）：
1、match pairs
2、check balance
3、invoke bidirectional-transaction-def
----
thread for update balance（option）
'''

ALIVE = QuoteManager()  # 存活Quote，线程安全
HISTORY = []


#
def okx_runner():
    c = okx_spot.OKX_SPOT()
    # all currencies
    currencies = c.flash_swap_get_currencies()
    while True:
        for i, o in currencies:
            q1 = c.flash_swap_fetch_flash_swap_buy_side(i, o, 10)
            q2 = c.flash_swap_fetch_flash_swap_sell_side(o, i, 10)
            tick = c.ticker_fetch(i, o)
            HISTORY.append(q1)
            ALIVE.add_quote(q1)
            HISTORY.append(q2)
            ALIVE.add_quote(q2)
            HISTORY.append(tick)
            time.sleep(1.5)


if __name__ == '__main__':
    ths = []
    # okx_runner
    runner_thread = threading.Thread(target=okx_runner)
    runner_thread.start()
    ths.append(runner_thread)
    # ...
    # monitor
    monitor_thread = threading.Thread(target=monitor_alive_and_history, args=(ALIVE, HISTORY))
    monitor_thread.start()
    ths.append(monitor_thread)
    # push
    push_thread = threading.Thread(target=update_influxdb, args=(HISTORY,))
    push_thread.start()
    ths.append(push_thread)
    #
    for t in ths:
        t.join()
