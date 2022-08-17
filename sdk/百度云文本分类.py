# encoding:utf-8
import requests
import argparse
import time

import xwtools as xw
# from xwtools.config_log import config
# import meilisearch
from loguru import logger
from tqdm import tqdm
from datetime import datetime, timedelta
from tqdm import tqdm
import redis
from util.redis_helper import redis_helper_class
import json
import csv
from util import pool_conn_utils


# !/usr/bin/env python
# -*- coding: utf-8 -*-

def get_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=XUkOfBc95VCStjkYgUrDDRV5&client_secret=S6vzGpIGNBKIiasZcTKiXr9sNyvUE0EG'
    response = requests.get(host)
    if response:
        j = response.json()
        for x in j:
            print(x, ':', j[x])


# !/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
from baidubce import bce_base_client
from baidubce.auth import bce_credentials
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce import bce_client_configuration


# 文章分类 Python示例代码
class ApiCenterClient(bce_base_client.BceBaseClient):

    def __init__(self, config=None):
        self.service_id = 'apiexplorer'
        self.region_supported = True
        self.config = copy.deepcopy(bce_client_configuration.DEFAULT_CONFIG)

        if config is not None:
            self.config.merge_non_none_values(config)

    def _merge_config(self, config=None):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, path, body, headers, params)

    def demo(self):
        path = b'/rpc/2.0/nlp/v1/topic'
        headers = {}
        headers[b'Content-Type'] = 'application/json;charset=UTF-8'

        params = {}

        params['access_token'] = '24.ec84ab6a73d26b92e5e102b509f731df.2592000.1660873951.282335-26747099'
        params['charset'] = 'UTF-8'

        body = '{\n\t\"title\":\"欧洲冠军联赛\",\n\t\"content\": \"欧洲冠军联赛是欧洲足球协会联盟主办的年度足球比赛，代表欧洲俱乐部足球最高荣誉和水平，被认为是全世界最高素质、最具影响力以及最高水平的俱乐部赛事，亦是世界上奖金最高的足球赛事和体育赛事之一。\"\n}'
        return self._send_request(http_methods.POST, path, body, headers, params)

    def fetch(self, title, content):
        path = b'/rpc/2.0/nlp/v1/topic'
        headers = {}
        headers[b'Content-Type'] = 'application/json;charset=UTF-8'

        params = {}

        params['access_token'] = '24.ec84ab6a73d26b92e5e102b509f731df.2592000.1660873951.282335-26747099'
        params['charset'] = 'UTF-8'

        body = '{\n\t\"title\":\"$_title_$\",\n\t\"content\": \"$_content_$\"\n}'
        body = body.replace('$_title_$', title[:40]).replace('$_content_$', content)
        res = self._send_request(http_methods.POST, path, body, headers, params)
        try:
            tags_dic = res.item.__dict__
            logger.info('成功一条{}:{}', tags_dic, title)
            return tags_dic
        except Exception as e:
            logger.warning('错误：{}', res)
            return None


#
endpoint = 'https://aip.baidubce.com'
ak = ''
sk = ''
config = bce_client_configuration.BceClientConfiguration(credentials=bce_credentials.BceCredentials(ak, sk),
                                                         endpoint=endpoint)
client = ApiCenterClient(config)
#
host = '192.168.0.3'
user = 'root'
password = 'brain@2022'
database = 'sci_brain'
port = 3306
mysql_pool = pool_conn_utils.pool_util([host, user, password, database, port])


# 检查是否存在
def check_not_exist(mongo_id, title):
    # 内存先筛一遍
    if mongo_id in finishSet:
        logger.warning('查到重复{},快速跳过', mongo_id)
        return False
    finishSet.add(mongo_id)
    # 再去数据库确认
    title_15 = title[:15]
    sql = '''select id from news_tags where mongo_id = '%s' or title = "%s"  ''' % (mongo_id, title)
    sql += ''' or title like"''' + title_15 + '''%"'''
    try:
        res = mysql_pool.fetch_one(sql)
        if not res:
            return True
        else:
            logger.warning('查到重复{},跳过', res)
            return False
    except Exception as e:
        logger.error(e)
        return False


# 入库 -> 就一条一条来吧，反正QPS也不高
def insert(**kwargs):
    mongo_id = kwargs['mongo_id']
    title = kwargs['title']
    content = kwargs['content']
    lv1_tag = kwargs['lv1_tag']
    lv2_tag = kwargs['lv2_tag']
    lv1_tag_list = kwargs['lv1_tag_list']
    lv2_tag_list = kwargs['lv2_tag_list']
    if not lv2_tag_list:
        lv2_tag_list = ''
    else:
        lv2_tag_list = str(lv2_tag_list)
    date = kwargs['date']
    sql = """ insert into news_tags (mongo_id,title,content,lv1_tag,lv2_tag,lv1_tag_list,lv2_tag_list,`date`) values ("%s","%s","%s","%s","%s","%s","%s","%s") """ % (
        mongo_id, title, content, lv1_tag, lv2_tag, lv1_tag_list, lv2_tag_list, date)
    mysql_pool.execute(sql)
    print('插入一条：', title, lv1_tag, lv2_tag)


def run(before_day: int = 0):
    #
    now = xw.TimeEtl.ge_now()
    mongoOp = xw.MongoOp('eitools', 'NewsMinerNewsHtml', label='weixin_mongo')
    filter_q = dict()
    if before_day:
        filter_q['date'] = {
            "$gte": xw.TimeEtl.time_str(xw.TimeEtl.str_time(xw.TimeEtl.before_day(now, before_day)))}
    data_iter = mongoOp.find_all_by_iter(
        filter_q,
        # {'_id': 1, 'title': 1, 'image': 1, 'src': 1, 'url': 1, "content": 1, 'created_time': 1, 'update_time': 1}
        {'html': 0}
    ).sort('date', -1).limit(500000)
    ret_list_num = 0
    for x in data_iter:
        ret_list_num += 1
        if ret_list_num % 100 == 0:
            logger.info('Already Download :%s' % ret_list_num)
        # ['id', 'title', 'content', 'tags', '']
        id = x['mongo_id'] = str(x['_id'])
        content = x['content'].replace('\n', ' ').replace('|', ' ').replace(' ', '').replace('\u3000', '')[:512]
        title = x['title'].replace('|', ' ').replace('\u3000', '').replace('''"''', "")
        data = x['date']
        # 库里没有才行
        if check_not_exist(id, title):
            tag_dic = client.fetch(title, content)
            if tag_dic:
                lv1_tag_list = [x.__dict__ for x in tag_dic['lv1_tag_list']]
                lv2_tag_list = [x.__dict__ for x in tag_dic['lv2_tag_list']]
                lv1_tag = '、'.join([x['tag'] for x in lv1_tag_list])
                lv2_tag = '、'.join([x['tag'] for x in lv2_tag_list])
                insert(mongo_id=id, title=title, content=content, lv1_tag=lv1_tag, lv2_tag=lv2_tag,
                       lv1_tag_list=lv1_tag_list,
                       lv2_tag_list=lv2_tag_list, date=data)
                print(tag_dic)


if __name__ == '__main__':
    global finishList
    finishSet = set()
    while 1:
        try:
            run(90)
        except Exception as e:
            logger.warning(e)
            logger.error('重新开始')
