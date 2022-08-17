import random
import time

import requests
import os
from xwtools import config

from util import pool_conn_utils
from util.postgres_helper import postgres_helper_class
from loguru import logger
import urllib
from tqdm import tqdm


def summary(text, brief=False):
    # cookie分别是: [wu,lin,tao,jiang]
    cookie_repo = [
        # 'BAIDUID=D8F2FF20D9A03472CEFD3349EED16136:FG=1; BIDUPSID=D8F2FF20D9A03472C5F75CB6BF115EE9; PSTM=1656242111; BDSFRCVID=LwtOJexroG06KkJDUpdmM4zzXSHDvd6TDYrEALqZNdWfoxAVJeC6EG0Pts1-dEu-EHtdogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=fnCDVIP-fIvbfP0k5tOqKPnH-UIs2pJlB2Q-5KL-fCjZM56kQhomQh-Ijh6EXPL8aTrhbxbdJJjoSJ53X4tahfIPDfrwK6Jg0mTxoUJXQCnJhhvGqt5KBUkebPRiJ-b9Qg-JbpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0M5DK0hIDlDjD2DjjM5pJfetQLa5n03J72HJOoDDvDKxOcy4LdjG5tapJ90eQR-xJdahCMJ4cyyhQ20-k73-Aq54RyJ6rTXDOubboAj4cshlQ0QfbQ0a5hqP-jW26aQfTwWn7JOpkRbUnxy50rQRPH-Rv92DQMVU52QqcqEIQHQT3m5-5bbN3ht6IHtnPtoC-KtDvbfP0kb-QM-t-X-fTbetJyaR0j5hbvWJ5TMC_wyRoJDJDv3J37XfuJMjQv0CTs-JQGShPC-tnbMRTB5qQxQUcubj7KLt5D3l02Vh7Ee-t2ynLVyxoh-tRMW20e0h7mWIbmsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJIjjC5e5j-eaKft5nfb5kX34JV5J7WKROkeU5JXM4pbt-qJJ-jMg6ELqbGaqTZ8Dbu2l7q2xAt5p5nBT5Ka25U2IocKJRpMT6R5MT1KTDkQN3TtRkO5bRiLlCbWfO5Dn3oyTbJXp0njb3ly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJPKtfJCsLb58MnT_KRopMtOhq4tehHRr-b39WDTOQJ7TtIQvjpce3J3fhfr32l6vQMvRbDPq-pbw-q5N8-jLX4ORb44bLJjZKxtq3mkjbPbbt66fstKzQf7Mb-4syP4eKMRnWnnTKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJzJCcjqR8Zjj0Bj6jP; BDUSS=JrSXFwVWxTTDQ1OXZlc25TT0RCU240clZCQXRnQWZ4TTJiNnFtZ35CflRIQlJqSUFBQUFBJCQAAAAAAAAAAAEAAABpAEpGveCw18Dxt~4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANOP7GLTj-xiZH; H_PS_PSSID=36554_36462_37117_37112_37143_36955_34812_36918_36805_37161_37135_26350_37095_22158; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; delPer=1; PSINO=6; BCLID=8500720025533470866; BA_HECTOR=2k80200k0h018ga1aha79t4k1hfmk2e16; ZFY=PwvvoA:AeXFIUTeWq:Bn:AoAgdZzgZ3lcmgIVs0HRGMJYw:C; RT="z=1&dm=baidu.com&si=im0i2pvcnk&ss=l6x0z0ft&sl=1&tt=3n&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=12a"; BDRCVFR[gltLrB7qNCt]=mk3SLVN4HKm; Hm_lvt_ebb78972b12bd9aef5154dd056e04b1b=1660646566; Hm_lpvt_ebb78972b12bd9aef5154dd056e04b1b=1660705081; Hm_lvt_1d14624ccaaf7fc81005e4565416f194=1660646566; Hm_lpvt_1d14624ccaaf7fc81005e4565416f194=1660705081; Hm_lvt_89be97848720f62fa00a07b1e0d83ae6=1660646566; Hm_lpvt_89be97848720f62fa00a07b1e0d83ae6=1660705081; Hm_lvt_56eff24245c08a007389c15d2e7ee0eb=1660646655; Hm_lpvt_56eff24245c08a007389c15d2e7ee0eb=1660705157; ab_sr=1.0.1_NTg4M2Y2NzQ1Y2FiYWI5YWEzYzExNjZmYmJiNTJiZjAwODRmMWRjMTg2ZWU4OTZiYmRjMjAyNjQyZWQ2NDFkNTQ5OTljMTNhZjQxNzlmOTQ4NDM3MmQxZDYwMmY3MjE1YTY5MGRjZGNlZjUwODllYTc5ZGQxMGMxOGY4ZGNlMjQxZmJmOGZmOGI3YmVhMmUxOTU3MzIwNzk5ZTE5ZjVhNQ==',
        'BAIDUID=D3B9A79D171EED61DB96F8E3004948A0:FG=1; BDUSS=nNod0E1cHNpcVU2YUx2RmUyYWtFYVBrZHdUb352dnVQV0tOdkVOeERvbHVJLXBpSVFBQUFBJCQAAAAAAAAAAAEAAADJL5BfacTqydnH4b~xZGUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG6WwmJulsJiU; BDUSS_BFESS=nNod0E1cHNpcVU2YUx2RmUyYWtFYVBrZHdUb352dnVQV0tOdkVOeERvbHVJLXBpSVFBQUFBJCQAAAAAAAAAAAEAAADJL5BfacTqydnH4b~xZGUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG6WwmJulsJiU; BIDUPSID=D3B9A79D171EED61DB96F8E3004948A0; PSTM=1657164484; newlogin=1; BDSFRCVID=29POJeC62xXejlODUW2VboKifm41rBbTH6f3DBulZ8TA5NT1OYszEG0Pbf8g0KublrsNogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tbuf_Dt5tCL3fP36q4To5PtebMoHetJyaR0HVxJvWJ5TMCo9W-o8hM4v3JtHLtjyWK5hWC-h-qoDShPCb6bULRLjWG7n36QwQn69h4OL3l02VboIe-t2ynLVhh5eWtRMW20e0h7mWIbmsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJIjj6jK4JKjHDOqxK; BDSFRCVID_BFESS=29POJeC62xXejlODUW2VboKifm41rBbTH6f3DBulZ8TA5NT1OYszEG0Pbf8g0KublrsNogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF_BFESS=tbuf_Dt5tCL3fP36q4To5PtebMoHetJyaR0HVxJvWJ5TMCo9W-o8hM4v3JtHLtjyWK5hWC-h-qoDShPCb6bULRLjWG7n36QwQn69h4OL3l02VboIe-t2ynLVhh5eWtRMW20e0h7mWIbmsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJIjj6jK4JKjHDOqxK; delPer=0; PSINO=6; ZFY=:BR1OOlUXsbil2:AbnzyeDf6p18fljqj3zPctyY9XlDHk:C; H_PS_PSSID=36560_36754_37112_36954_36949_36917_37128_37131_26350_36863_37022; ZD_ENTRY=bing; BAIDUID_BFESS=D3B9A79D171EED61DB96F8E3004948A0:FG=1; Hm_lvt_56eff24245c08a007389c15d2e7ee0eb=1660716677; Hm_lpvt_56eff24245c08a007389c15d2e7ee0eb=1660716677; ab_sr=1.0.1_NmZkYmNmYjljYmYzMTYwZWVjODQyODE0ZTMzNTMwZWE2YWExODY5Zjk3ZDRhNTY4MDVmNTQ0NjgwZTA4NjE0MGIxMTkwOWJkMjQ1MGU3MGNmOGI4Njc5MWRlMTc3YWQyNTNmMTFmMzMxOTE3OGFhZmUyYTdmNjc2NGU5OGI4YmVkZDYxNTk5YTAxYzg1Y2ExMDIzODE3YjVmMTA4NGI1Yg==; RT="z=1&dm=baidu.com&si=lto5nppoiw&ss=l6x932t9&sl=2&tt=bs0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=dfm"',
        'BIDUPSID=59777252038AAFE8CBA385A62E4D4479; PSTM=1657007320; BAIDUID=59777252038AAFE8BAD7A546B7128BEF:FG=1; BDUSS=UQ4OH5xbUxxMXM1VTFLbjlKMndScnpsbnB4eXlGS0wwckgxS3EtckZaUU5OTzlpSVFBQUFBJCQAAAAAAAAAAAEAAAAMQ3BuU3VucmlzaW5nZXZlcgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA2nx2INp8diN; BDUSS_BFESS=UQ4OH5xbUxxMXM1VTFLbjlKMndScnpsbnB4eXlGS0wwckgxS3EtckZaUU5OTzlpSVFBQUFBJCQAAAAAAAAAAAEAAAAMQ3BuU3VucmlzaW5nZXZlcgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA2nx2INp8diN; BDSFRCVID=NyCOJeC62u-g2cQDgd7XMqlKfmKbcgrTH6f3k1QTwD6_JgxrE8HKEG0PXM8g0Ku-hnxxogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tJuHVIIKfIvDqTrP-trf5DCShUFsqT3iB2Q-XPoO3Kt-8x5nQ5QZMp-VjqbUX4biWaT9WfbgylRp8P3y0bb2DUA1y4vp5hJ2LeTxoUJ2--taot5mqf7F3R_ebPRiJ-b9Qg-JbpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hC_4e5u-e5PVKgTa54cbb4o2WbCQ0lcN8pcN2b5oQTOBXRo20Tok256a_4O6yR3vOU5OhlOUWfAkXpJvQnJjt2JxaqRCKMOjVl5jDh3MKnOLWqoJexvwQj6y0hvctb3cShPm0MjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDH-OJ6tttJ3KB6rtKRTffjrnhPF3ehFFXP6-35KHMgQ9-prv3PcBVx3PjJbRWtb3hUJDth37JDFea-KXtx5SoCO8j6Jojj_qW-oxJp8OMnbMopvaHx8KstjvbURvDP-g3-AJQU5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-j5JIEoD_-fII-bKvPKITD-tFO5eT22-usXK6d2hcHMPoosItCXlojQbIfeaOatRJUyCviaM5vafbUoqRHXnJi0btQDPvxBf7pKa72bq5TtUJMqPtlWJoMqfkN3lQyKMnitKv9-pP2LpQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKujT8Be5cQjHRbet3KbI680488Kb7VbprwLUnkbfJBDl_LK5j2LmnM0I39B4jSOnQzyP5jbnD7yajhJ-PDLGnfKIQ7WJ3WqlK9yMRpQT8rW-FOK5Oib4j3Wtnyab3vOIOTXpO1jh8zBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksDMDtqtJHKbDJ_KIKtxK; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BA_HECTOR=0kaha001812g018g2h2gdt4l1hfovbu16; ZFY=4NJaqny45I9hfVUWDOGlsJFe79p5jzMraY0UKTvDO5w:C; BAIDUID_BFESS=59777252038AAFE8BAD7A546B7128BEF:FG=1; BDSFRCVID_BFESS=NyCOJeC62u-g2cQDgd7XMqlKfmKbcgrTH6f3k1QTwD6_JgxrE8HKEG0PXM8g0Ku-hnxxogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF_BFESS=tJuHVIIKfIvDqTrP-trf5DCShUFsqT3iB2Q-XPoO3Kt-8x5nQ5QZMp-VjqbUX4biWaT9WfbgylRp8P3y0bb2DUA1y4vp5hJ2LeTxoUJ2--taot5mqf7F3R_ebPRiJ-b9Qg-JbpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hC_4e5u-e5PVKgTa54cbb4o2WbCQ0lcN8pcN2b5oQTOBXRo20Tok256a_4O6yR3vOU5OhlOUWfAkXpJvQnJjt2JxaqRCKMOjVl5jDh3MKnOLWqoJexvwQj6y0hvctb3cShPm0MjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDH-OJ6tttJ3KB6rtKRTffjrnhPF3ehFFXP6-35KHMgQ9-prv3PcBVx3PjJbRWtb3hUJDth37JDFea-KXtx5SoCO8j6Jojj_qW-oxJp8OMnbMopvaHx8KstjvbURvDP-g3-AJQU5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-j5JIEoD_-fII-bKvPKITD-tFO5eT22-usXK6d2hcHMPoosItCXlojQbIfeaOatRJUyCviaM5vafbUoqRHXnJi0btQDPvxBf7pKa72bq5TtUJMqPtlWJoMqfkN3lQyKMnitKv9-pP2LpQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKujT8Be5cQjHRbet3KbI680488Kb7VbprwLUnkbfJBDl_LK5j2LmnM0I39B4jSOnQzyP5jbnD7yajhJ-PDLGnfKIQ7WJ3WqlK9yMRpQT8rW-FOK5Oib4j3Wtnyab3vOIOTXpO1jh8zBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksDMDtqtJHKbDJ_KIKtxK; delPer=0; PSINO=6; H_PS_PSSID=37146_36552_36625_36642_37115_36977_34813_36917_37003_36807_36779_36789_37127_37136_26350_36863; Hm_lvt_56eff24245c08a007389c15d2e7ee0eb=1660721760; Hm_lpvt_56eff24245c08a007389c15d2e7ee0eb=1660721760; ab_sr=1.0.1_MmYzZjNhOWNiNjkxNzk5MjYzY2Y0ZDlmYzIyNGRjYTM1MDhmOGIxOWVjMWZjZTg2ZWVlZjAwNTRhZDM3NjUzYjU5Njc5YjZiNDA2YTA4M2Y3MDY0ODEzMWI1MzBmZmM5ODQxOWM5ZDFhMjUwNTNiNDA3OGUwNjkyODc5YjNhOTU2MWExYzAzN2RlMzYyNTlkYTM5MTZjZGRmZjI1NDdjYg==; RT="z=1&dm=baidu.com&si=gl5sbtv0pwt&ss=l6xauuqb&sl=3&tt=3pq&bcn=https://fclog.baidu.com/log/weirwood?type=perf&ld=1ef1"',
        'PSTM=1660557459; BAIDUID=5941F520FAB450EC3235E1AB9B4F2907:FG=1; BIDUPSID=42948CC72041D9A5A8DC8D52F21EA9E4; ZFY=ED4Xcvd:BEUSRnZE2ZzndRvO5IxxyPhVbIVQkWJLPUAk:C; delPer=0; PSINO=6; H_PS_PSSID=36552_36624_36641_36973_36955_34813_36917_36570_37163_37131_37055_26350; BAIDUID_BFESS=5941F520FAB450EC3235E1AB9B4F2907:FG=1; BDUSS=41SWo3Q2xKaUUwVDV4amk3TGlkTlNJZUx1aVBUNjdTb3FFNVlhQ2NUdHZiU05qSUFBQUFBJCQAAAAAAAAAAAEAAADqIHEYOTYxMTY1ODg1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG~g-2Jv4PtidE; BDUSS_BFESS=41SWo3Q2xKaUUwVDV4amk3TGlkTlNJZUx1aVBUNjdTb3FFNVlhQ2NUdHZiU05qSUFBQUFBJCQAAAAAAAAAAAEAAADqIHEYOTYxMTY1ODg1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG~g-2Jv4PtidE; Hm_lvt_56eff24245c08a007389c15d2e7ee0eb=1660721642; Hm_lpvt_56eff24245c08a007389c15d2e7ee0eb=1660721642; ab_sr=1.0.1_M2Y4OWJjYjJkZTdmNmNkYjk1OTBiMzI1MDI5ZjRjMDdkNTAwMzdlZGJiZmQ0ZGViYTljNGQ5Y2Y4MWM0MjZiZWQ5ODEwM2I2NTIzMzMzNmQ2MTM1N2I3MDhiODAwYzVlYmYzMWMyMTY0ZmQ5NWVmYzMzYWFkNWQ1ZjU0MjM5ZDA0NzNjNDljZWYyOTIxODE4NTQxNTZhYTUzOTM0OGRmZg==; RT="z=1&dm=baidu.com&si=9pvpcsty3i9&ss=l6xasbwl&sl=4&tt=k7e&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1ult"',
    ]
    choose_cookie = random.choice([0, 1])
    logger.info('选中cookie编号为:{}', choose_cookie)
    choose_cookie = cookie_repo[choose_cookie]
    #
    url = "https://wenxin.baidu.com/moduleApi/portal/api/invoke"
    payload = 'text=%E6%B7%B1%E5%9C%B3%E8%B6%85%E8%84%91&modelId=1&minDecLen=4&seqLen=512&topp=0&penaltyScore=1&apiId=20023&taskPrompt=1.0%2CSummarization%2C1.0%2C1.0%2C%2C%2C%2C0%2C1'
    headers = {
        'Referer': 'https://wenxin.baidu.com/moduleApi/ernie3',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://wenxin.baidu.com',
        'Connection': 'keep-alive',
        'Cookie': choose_cookie,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    # 转url编码
    text_url = urllib.parse.quote(text)
    payload = payload.replace('%E6%B7%B1%E5%9C%B3%E8%B6%85%E8%84%91', text_url)
    # 如需超简版:
    if brief:
        delete = '&taskPrompt=1.0%2CSummarization%2C1.0%2C1.0%2C%2C%2C%2C0%2C1'
        payload = payload.replace(delete, '')
    response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
    print(response.json())
    res_dict = response.json()
    if res_dict['msg'] == "请稍后重试":
        logger.warning("请稍后重试:{} >> {}", text[:30], res_dict)
        return
    if res_dict['msg'] == "success":
        return res_dict['data']['result']
    if res_dict['code'] == 1:
        logger.warning("失败:{} >>> {}", res_dict['msg'], text[:30])
        return
    logger.error("出现异常：{}", response.text)
    return


def run(limit):
    conf_str = 'brain_postgres'
    host = config(conf_str, 'host')
    user = config(conf_str, 'user')
    password = config(conf_str, 'pass')
    port = config(conf_str, 'port')
    database = config(conf_str, 'db')
    pool = pool_conn_utils.pool_util([host, user, password, database, port], db_type='postgresql')
    logger.info('接入postgres：{}:{}/{}', host, port, database)
    q = 'select * from recsys_item order by day desc limit %s' % limit
    item_list = pool.fetch_all(q)
    logger.info('拉取数据：{}条', len(item_list))
    fail_count = 0
    for item in tqdm(item_list):
        content = item['content']
        mongo_id = item['mongo_id']
        abstract = item['abstract']
        if abstract:
            logger.info("已存在跳过一条:{}", abstract)
            continue
        abstract = summary(content[:1000], brief=False)
        if not abstract:
            fail_count += 1
            continue
        if len(abstract) < 8:
            fail_count += 1
            continue
        q = """update recsys_item set abstract = '%s' where mongo_id = '%s' """ % (abstract, mongo_id)
        pool.execute(q)
        logger.success('插入一条：{}', mongo_id)
        if fail_count > 50:
            logger.error('连续错误超过{}次，请注意！', fail_count)
            quit()
        fail_count = 0


def test_once():
    text = """是国家经济发展的“顶梁柱”。经济大省要勇挑大梁，发挥稳经济关键支撑作用。落实好稳经济一揽子政策，挖掘自身政策潜力，保市场主体激发活力，保障物流主干道、微循环畅通，稳定产业链供应链。稳经济也是稳财源。6省里4个沿海省在地方对 财政净上缴中贡献超过6成，要完成财政上缴任务。  中国政法大学施正文教授告诉第一财经，受疫情等影响，今年经济财政形势比较严峻，经济大省应该勇挑大梁，多措并举完成对 财政净上缴任务，这对支撑国家财力和 财政对中西部地区转移支付十分重要，支持欠发达地区“保基本民生、保工资、保运转”，体现经济大省担当。  当前中国财政体制下， 与地方采取分税制，来划分各级 收入。经济大省财政收入规模高， 财政相应从中获得的收入也更高，初次分配中， 财政拿到全国近半财政收入（即一般公共预算收入）。但为了均衡区域发展，推动基本公共服务均等化， 财政收入大部分最终通过转移支付形式，再分配给各省，其中又以欠发达的中西部、东北地区为主，有效地均衡地区间财力差异，有利于区域协同发展。  粤开证券首席经济学家罗志恒告诉第一财经，目前地方对 财政净贡献一般是以各省为 财政创造的财政收入与 返还该省份金额差额。目前官方公布的数据只能计算到2019年各地对 财政净贡献金额。  根据罗志恒计算，2019年全国只有六省三市对 财政净贡献，其中广东以净贡献8307亿元居各省之首，上海以8202亿元紧随其后，北京以7310亿元位居第三。江苏（4091亿元）、浙江（3274亿元）、山东（2152亿元）、天津（2136亿元）、福建（427亿元）、辽宁（67亿元）也对 财政净贡献。  今年国务院十分强调财政强省要发挥保障国家财力主力的作用，这跟当前经济财政形势有关。  受疫情散发、大规模退税减税降费、土地市场低迷等影响，包括 财政在内的全国财政收入罕见出现下滑。
    财政部数据显示，今年上半年全国一般公共预算收入约10.5万亿元，按自然口径计算下降10.2%，不过扣除增值税留抵退税因素后3.3%。其中， 一般公共预算收入约4.8万亿元，扣除留抵退税因素后增长1.7%，按自然口径计算下降12.7%。
    地方上除了山西等几个资源型省份收入出现大幅增长外，大多数省份收入也出现下滑，其中受疫情等冲击较大的东部发达省市，收入受到明显冲击。
    为了给企业纾困和保民生，今年 财政动用万亿级“家底”，来加大对地方转移支付规模（约10万亿元），但要完成这笔巨额转移支付规模，离不开财政大省对 财力净贡献。
    7月7日， 在福建主持召开东南沿海省份 主要负责人座谈会上表示，当前正处于经济恢复的关键时间点。东南沿海5省市（福建、上海、江苏、浙江、广东）经济体量占全国1/3以上，财政收入占比近4成，在地方对 财政净上缴中贡献近8成，有力支撑了国家财力和 财政对中西部地区转移支付。
     要求，要继续挑起国家发展、稳经济的大梁，发挥保障国家财力的主力作用。在做好疫情防控的同时，进一步打通产业链供应链堵点，推动经济运行尽快回归正常轨道，努力稳增长稳财源。
    此次会议则进一步明确，6省里4个沿海省（广东、江苏、浙江、山东）要完成财政上缴任务。目前官方尚未披露财政净上缴 的省需要完成上缴任务具体金额。施正文认为，这可能是在各地去年净上缴金额基础上，保持一定的增长。
    财政部数据显示，2022年 对地方转移支付预计近9.8万亿元，规模为历年来最大；从增幅来看，2022年 对地方转移支付比上年增加约1.5万亿元，增长18%，增幅为近年来最高。
    根据国家统计局数据，今年上半年广东一般公共预算收入为6730亿元，扣除留抵退税因素后同比下降0.5%，按自然扣除同比下降11.4%；浙江省一般公共预算收入4984亿元，扣除留抵退税因素同比增长4.2%，按自然口径同比下降6.2%；江苏省一般公共预算收入为4639亿元，扣除留抵退税因素同比下降5.8%，按自然口径同比下降17.9%；山东省一般公共预算收入为3950亿元，扣除留抵退税因素同比增长6.3，按自然口径同比下降8.2%。
    随着增值税留抵退税减收因素逐步减小以及经济稳步复苏，专家预计，上述东部省份财政收入降幅持续缩窄，收入稳步增长，这为完成 财政净上缴任务奠定基础。
    施正文表示，东部经济大省经济韧性更强，抗风险能力更大，“家底”更厚，回旋余地更大，因此经济大省勇挑大梁，努力完成任务，保障全国财力稳定。
    除了财力净贡献省份努力完成任务外，专家认为，其他依赖 财政转移支付的省份也应多措并举，努力做到财政收支平衡。
    会上， 说， 财政对地方转移支付已基本下达，各省要坚持 过紧日子，盘活财政存量资金，保持财政收支平衡，加大财力下沉，保障基层“三保”尤其是保基本民生支出、保基层工资发放。
        """
    summary(text.replace(' ', '')[:500])


if __name__ == '__main__':

    # test_once()

    while 1:
        run(800)
        logger.info('一轮结束')
        time.sleep(100)
