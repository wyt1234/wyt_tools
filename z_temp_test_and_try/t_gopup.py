


import gopup as gp
df_index = gp.energy_oil_hist()
print(df_index)

import gopup as gp
df_index = gp.zhihu_hot_search_list()
print(df_index)


import gopup as gp
df_index = gp.zhihu_hot_list()
print(df_index)

import gopup as gp
df_index = gp.nicorn_company()
print(df_index)

import gopup as gp
index_df = gp.google_fact_check(keyword="口罩", offset=0, limit=100, hl=None)
print(index_df)


import gopup as gp
cookie = 'BAIDUID=D8F2FF20D9A03472CEFD3349EED16136:FG=1; BIDUPSID=D8F2FF20D9A03472C5F75CB6BF115EE9; PSTM=1656242111; HMACCOUNT=CE72F2C991F87F84; BDUSS=k92MkUzQjNDWlV-NEhBU3pZOWdDdkhibWRzZ2QzLVhwbXcwVk8yd2tBRmptWlZqSVFBQUFBJCQAAAAAAAAAAAEAAABpAEpGveCw18Dxt~4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGMMbmNjDG5jR; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BDSFRCVID=hR_OJeC62w2JSH6j7r5IhMW_sZAsryJTH6ao9zLmAAs8SpNt1dfoEG0PWU8g0KAMKDpcogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tR4f…NjZTk3MGU2NjdjM2I5N2IzMWY2MDM4NzNiZjE1Zg==; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a04204956266dOkZjqD5aqSGiH9Y3JCbGKvrYqbtUa0tc%2F9wAHKcN67JCimBXhhSTxd5B9TTgSjtLOs2XmQ1H2%2FDWCcfCX7CpoiPLqfhj%2Bm9VbYjjqGlvlRfEiE5Qrd%2F9gnCNM9Debgn7GKMGyuxiljlnJzM5PL80CNUVA2W%2F%2B3uYHwTjxM8VlXAlXc1lV%2Fu%2Bp5sJmJV4pM55UOgJR2RDg0OqwOllsW3wX6aLM4Cc75NFQNMnTpMqDijiRnHw18NPaV0fLPNjLVKrTp26s%2BCRsz8ZnTOqFfzYTSIFo%2BQMdsIC25p9gpRWuzV%2FTa3NI0hdXpT8%2BHJkkDE61608919684901031594609416165022; bdindexid=2b1n48fp3v7dc51sp6pikumk83'  # 此处请用单引号
index_df = gp.baidu_media_index(word="神州飞船", start_date='2022-01-01', end_date='2022-01-04', cookie=cookie)
print(index_df)



import gopup as gp
index_df = gp.google_index(keyword="口罩", start_date='2022-09-10T10', end_date='2022-09-13T23')
print(index_df)


import gopup as gp
index_df = gp.toutiao_index(keyword="口罩", start_date='20201016', end_date='20201022', app_name='aweme')
print(index_df)


import gopup as gp
index_df = gp.toutiao_city(keyword="口罩", start_date='20221016', end_date='20221122', app_name='aweme')
print(index_df)





import gopup as gp
df = gp.weibo_index(word="疫情", time_type="1hour")
print(df)

