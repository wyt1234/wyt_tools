import time

import okx_spot
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
    currencies = c.get_currencies()
    while True:
        for i, o in currencies:
            q1 = c.flash_swap_fetch_flash_swap_buy_side(i, o, 10)
            q2 = c.flash_swap_fetch_flash_swap_sell_side(o, i, 10)
            HISTORY.append(q1)
            ALIVE.add_quote(q1)
            HISTORY.append(q2)
            ALIVE.add_quote(q2)
            time.sleep(3)


def monitor_alive_and_history():
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

    while True:
        # 执行ALIVE清理
        ALIVE.remove_dead_quotes()
        alive_count = len(ALIVE.live_quotes)
        history_count = len(HISTORY)
        # clear_console()
        print_table(alive_count, history_count)
        time.sleep(1)


if __name__ == '__main__':
    ths = []
    # okx_runner
    runner_thread = threading.Thread(target=okx_runner)
    runner_thread.start()
    ths.append(runner_thread)
    # ...
    # monitor
    monitor_thread = threading.Thread(target=monitor_alive_and_history)
    monitor_thread.start()
    ths.append(monitor_thread)
    # 等待线程执行完成
    for t in ths:
        t.join()
