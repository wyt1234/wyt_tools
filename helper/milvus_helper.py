import datetime
import json

import loguru
import numpy as np
import requests
from loguru import logger
from tqdm import tqdm

from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)
from xwtools import config


class milvus_helper_class:
    def __int__(self):
        return

    # 创建索引
    def create_index(self):
        return

    # 创建库
    def create_collection(self):
        return

    # 删除超过n天的数据
    def rm_old(self, collection_name, ago=3 * 30):
        # 计算 3 个月以前的时间戳
        three_months_ago = datetime.datetime.now() - datetime.timedelta(days=ago)
        three_months_ago_timestamp = int(three_months_ago.timestamp())
        # 搜索距离今天 3 个月以前的资讯
        expr = f"timestamp < {three_months_ago_timestamp}"
        # 获取集合对象
        collection = Collection(collection_name)
        # 定义需要检索的字段
        output_fields = ["mongo_id"]
        # 查询符合条件的实体
        search_result = Collection(collection_name).query(expr, output_fields=output_fields)
        # 获取实体的 mongo_id
        entity_mongo_ids = [entity.mongo_id for entity in search_result]
        # 如果存在要删除的实体
        if entity_mongo_ids:
            # 构建删除表达式
            delete_expr = f"mongo_id in {entity_mongo_ids}"
            # 删除符合条件的实体
            delete_result = collection.delete(delete_expr)
            # 输出删除成功的数据条目数量
            print(f"Deleted {delete_result.delete_count} items successfully.")
        else:
            print("No items to delete.")
        return
