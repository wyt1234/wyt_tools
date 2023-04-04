



import akshare as ak

nicorn_company_df = ak.nicorn_company()
print(nicorn_company_df)



import akshare as ak

maxima_company_df = ak.maxima_company()
print(maxima_company_df)


import akshare as ak
car_gasgoo_sale_rank_df = ak.car_gasgoo_sale_rank(symbol="品牌榜", date="202211")
print(car_gasgoo_sale_rank_df)





import akshare as ak


cookie = 'BAIDUID=D8F2FF20D9A03472CEFD3349EED16136:FG=1; BIDUPSID=D8F2FF20D9A03472C5F75CB6BF115EE9; PSTM=1656242111; HMACCOUNT=CE72F2C991F87F84; BDUSS=k92MkUzQjNDWlV-NEhBU3pZOWdDdkhibWRzZ2QzLVhwbXcwVk8yd2tBRmptWlZqSVFBQUFBJCQAAAAAAAAAAAEAAABpAEpGveCw18Dxt~4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGMMbmNjDG5jR; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BDSFRCVID=hR_OJeC62w2JSH6j7r5IhMW_sZAsryJTH6ao9zLmAAs8SpNt1dfoEG0PWU8g0KAMKDpcogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tR4f…NjZTk3MGU2NjdjM2I5N2IzMWY2MDM4NzNiZjE1Zg==; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a04204956266dOkZjqD5aqSGiH9Y3JCbGKvrYqbtUa0tc%2F9wAHKcN67JCimBXhhSTxd5B9TTgSjtLOs2XmQ1H2%2FDWCcfCX7CpoiPLqfhj%2Bm9VbYjjqGlvlRfEiE5Qrd%2F9gnCNM9Debgn7GKMGyuxiljlnJzM5PL80CNUVA2W%2F%2B3uYHwTjxM8VlXAlXc1lV%2Fu%2Bp5sJmJV4pM55UOgJR2RDg0OqwOllsW3wX6aLM4Cc75NFQNMnTpMqDijiRnHw18NPaV0fLPNjLVKrTp26s%2BCRsz8ZnTOqFfzYTSIFo%2BQMdsIC25p9gpRWuzV%2FTa3NI0hdXpT8%2BHJkkDE61608919684901031594609416165022; bdindexid=2b1n48fp3v7dc51sp6pikumk83'  # 此处请用单引号
text = '1670396725293_1670483940269_V3JWKjhUXvslCc8ZNEsDxsqmMSyN9zs8xP/V2uPC8f/Reg39DL9iUjdusOrqZIHC7fIE3helPKGT52J2wrY0ecLjmWwBMQDNLyJJmpcouQ3JaK06yuYVPQmJBkdl8oBvSZGn2ZNeOtQmFHG5VMeMKg+SG85UBiGv0xbk4mQFyXmSHCueQ7PnK8nYkS+2hUi7RGzc9ECcPwABG0z+zUUsEVqdDh0OpnMHqkdr4hLmjTuTPsCW3ewfguRYXkj2g6zHsOtJb3/RfsnWL1jbOrA+EI8Go2gjU2NgfieI0RQuxGp6U6ZCZjk/QTHD64DIcbl/fe1x6MZVlA51jH7m/K9qPJ6hmPDuWhkaE8b+1p4/sdJ49LBtvPslqMJ1B6LHpbl/1RIfqgqKfTvF4OAF65gGku284Gj/PPMMIh8pOpjCrFM='
baidu_info_index_df = ak.baidu_info_index(word="螺纹钢", start_date='2022-07-03', end_date='2022-12-01', cookie=cookie,
                                          text=text)
print(baidu_info_index_df)
