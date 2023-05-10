import okx_spot

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


ALIVE = []
HISTORY = []

#
def okx_runner():
    # all currencies
    currencies = okx_spot.get_currencies()
