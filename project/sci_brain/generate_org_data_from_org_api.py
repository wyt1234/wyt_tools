import datetime
import json
from typing import List
import requests
import traceback
from elasticsearch import Elasticsearch
import logging
import os
from multiprocessing import Pool
from pymongo import MongoClient, UpdateOne
from collections import defaultdict


org_detail_url = "http://datacenter.aminer.cn/gateway/api/v2/organization/detail?id=%s"
org_info_url = "https://apiv2.aminer.cn/magic?a=GetOrgInfo__orgapi.get___"

data_center_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhaWQiOiI2MmExOTliMzcwNmZkOTI2NzA5ZjRiMWQiLCJhdWQiOlsiOWFlNTk2NmEtNjhiYy00MWMxLWFlNTYtZjFlZDc5ZjQzODNlIl0sImNpZCI6IjlhZTU5NjZhLTY4YmMtNDFjMS1hZTU2LWYxZWQ3OWY0MzgzZSIsImV4cCI6MTY2OTUzMjA1MiwiZ2VuZGVyIjowLCJpYXQiOjE2Njk1Mjg0NTIsImlkIjoiNjJhMTk5YjM3MDZmZDkyNjcwOWY0YjFkIiwiaXNzIjoib2F1dGguYW1pbmVyLmNuIiwianRpIjoiMmFhZGMzYTAtN2IxNC00NTY1LTkyMjMtNzIxOTE1YWEwNmMzIiwibmJmIjoxNjY5NTI4NDUyLCJuaWNrbmFtZSI6IlNIRU5aSEVOYWRtaW4iLCJzdWIiOiI2MmExOTliMzcwNmZkOTI2NzA5ZjRiMWQiLCJ0IjoiUGFzc3dvcmQifQ.iNSNp3oyCzG9_cFRj4TuZGZfTSEuSZy1YoI2GwBZGwMsRQNE9TWimQs-OF4cRIzyDFJ_2i9bVo4L5spJNXFVItB3pXIz86hGlo6NBFKAj2Zxtz_uPSwAUhGfjgmaGGhTGvE2BOMm52N9nRC9R3LhSLzxJtPUd2zWT9dKFLJ-pN-anbqZmzNx-YbqrtPBtuBaUYJuODLcq7kvvNSO32LpHU_APRcBqVa1J1YN1-ADg6saHeCe2tXRjVLw_DkMJ7kPqGguEHZgg04y0e7CFH_koHLcfylX7NuKaCa9YVgpZJkfu1GIU9Ur3lOSbFMeNju7WKs0IElWvg_Kkg-EoFY6pA"

person_v9_index = "person_details_v9"


es = Elasticsearch(hosts='http://192.168.0.14:9200/', timeout=30, max_retries=3, retry_on_timeout=True)


def get_logger(parent_dir: str, name: str):
    logger = logging.getLogger(name)
    # 创建一个handler，用于写入日志文件
    log_name = f'{datetime.datetime.now().date()}_{name}.log'
    filename = os.path.join(parent_dir, log_name)
    fh = logging.FileHandler(filename, mode='w+', encoding='utf-8')
    # 定义输出格式(可以定义多个输出格式例formatter1，formatter2)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    # 定义日志输出层级
    logger.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    # 给logger对象绑定文件操作符
    logger.addHandler(fh)
    return logger


def get_org_infos_by_org_ids(orgs: List[dict], sz_org_list: List[str], org_process_logger):
    payload_info = {
        "action": "orgapi.get",
        "parameters": {
            "id": "",
            "need_details": True
        },
        "schema": {
            "person": [
                "name",
                "id"
            ]
        }
    }
    org_infos = []
    t0 = datetime.datetime.now()
    org_process_logger.info(f"start to get org data from org_api, now: {t0}")
    for index, org in enumerate(orgs):
        org_id = org["org_id"]
        org_process_logger.info(f"get org_id: {org_id}, index: {index + 1}")
        fields = org["fields"]
        org_detail_response = requests.get(org_detail_url % org_id, headers={"Authorization": data_center_token})
        if org_detail_response.status_code != 200:
            continue
        try:
            resp = org_detail_response.json()
        except Exception as e:
            org_process_logger.error(f"get org data detail error, org_id: {org_id}, error: {e}")
            continue

        org_detail_data = resp.get("data", {})
        if org_detail_data is None:
            org_process_logger.error(f"fuck no detail, org_id: {org_id}")
            continue
        org_dict = {
            "org_name": org_detail_data.get('name', ""),
            "org_nameZh": org_detail_data.get('name', ""),
            "image": org_detail_data.get('image', ""),
            'aminer_id': org_id,
            "n_citation": "",
            "n_papers": "",
            "location": "",
            "location_zh": "",
            "persons": [],
            "is_sz": 0,
            'fields': fields,
            'project_id': "cells and genes"
        }
        org_infos.append(org_dict)
        payload_info['parameters']['id'] = org_id
        org_info_response = requests.post(org_info_url, data=json.dumps([payload_info]))
        if org_info_response.status_code != 200:
            continue
        try:
            resp = org_info_response.json()
        except Exception as e:
            org_process_logger.error(f"get org data info error, org_id: {org_id}, error: {e}")
            continue
        org_info_data = resp.get("data", [{}])[0]
        org_info_detail_map = org_info_data.get("details", {})
        orgs = org_info_data.get("orgs", [])

        # 补全 citation 和 papers
        citation = org_info_detail_map.get('citation', 0)
        pub_count = org_info_detail_map.get('pub_count', 0)
        org_dict["n_citation"] = citation
        org_dict["n_papers"] = pub_count

        # 补全 persons
        persons = []
        for author_map in org_info_detail_map.get("authors", []):
            persons.append({"aminer_id": author_map.get("id", ""), "name": author_map.get("name", "")})
        org_dict["persons"] = persons

        # 补全 location
        for org_row in orgs:
            org_row_detail = org_row.get("details", {})
            en_location = org_row_detail.get("en", {})
            zh_location = org_row_detail.get("zh", {})
            org_dict["location"] = en_location.get("country", "") + en_location.get("city", "")
            org_dict["location_zh"] = zh_location.get("country", "") + zh_location.get("city", "")

        # 判断机构是否属于深圳
        if org_dict['org_name'].lower().find('shenzhen') != -1 or org_dict['org_nameZh'].find('深圳') != -1:
            org_dict['is_sz'] = 1
        if org_dict['is_sz'] == 0:
            for sz_org in sz_org_list:
                if (org_dict['org_name'].find(sz_org) != -1 and len(sz_org) / len(org_dict['org_name']) * 100 > 40) or (org_dict['org_nameZh'].find(sz_org) != -1 and len(sz_org) / len(org_dict['org_nameZh']) * 100 > 40):
                    org_dict['is_sz'] = 1
                    break

    t1 = datetime.datetime.now()
    org_process_logger.info(f"end to get org data from org_api, now: {t1}, cost_time: {(t1 - t0).total_seconds()}")
    return org_infos


def insert_org_data_by_org_ids(orgs: List[dict], sz_org_list: List[str], start: int, end: int):
    mongo_client = MongoClient(
        host="192.168.0.42",
        port=27017,
        username="admin",
        password="gkx_2022",
        authSource="admin",
    )
    org_final_col = mongo_client["industry_graph"]["org_final"]

    t0 = datetime.datetime.now()
    org_process_logger = get_logger(parent_dir=log_path, name=f"cell_and_gene_org_{start}_{end}")
    org_process_logger.info(f"start to get org_data by api and insert org data, start :{start}, end: {end}, now: {t0}")
    try:
        org_infos = get_org_infos_by_org_ids(orgs, sz_org_list, org_process_logger)
        org_final_col.insert_many(org_infos)
    except Exception as e:
        org_process_logger.error(f"get org infos faild, error: {traceback.format_exc()}")
    t1 = datetime.datetime.now()
    org_process_logger.info(f"end to get org_data by api and insert org data, start :{start}, end: {end}, now: {t1}, cost_time: {(t1 - t0).total_seconds()}")


def get_org_data_by_org_ids(input_path: str, sz_org_path: str):
    t0 = datetime.datetime.now()
    print(f"start to get org_data by org_ids, now: {t0}")
    batch_cnt = 100
    pool = Pool(16)
    sz_org_list = []
    data = json.loads(open(sz_org_path, 'r').read())
    for i in data['data']:
        sz_org_list += [j for j in i['aliases']]

    org_list = []
    with open(input_path, "r") as f:
        while True:
            s = f.readline()
            if not s:
                break
            s = s.strip("\n")
            org_data = json.loads(s)
            org_list.append(org_data)

    for step_index in range(len(org_list))[::batch_cnt]:
        batch_orgs = org_list[step_index:step_index+batch_cnt]
        pool.apply_async(insert_org_data_by_org_ids, args=(batch_orgs, sz_org_list, step_index, step_index+batch_cnt))

    pool.close()
    pool.join()
    t1 = datetime.datetime.now()
    print(f"end to get org_data by org_ids, now: {t1}, cost_time: {(t1 - t0).total_seconds()}")


def get_person_org_ids(person_ids: List[str], org_id_field_map: dict, person_id_fields_map: dict, org_logger):
    """
    根据学者id列表获取学者的机构的id
    """
    batch_cnt = 10
    t0 = datetime.datetime.now()
    org_logger.info(f"start to get person, person_len: {len(person_ids)}, now: {t0}")
    results = []
    for step_index in range(len(person_ids))[::batch_cnt]:
        batch_person_ids = person_ids[step_index:step_index+batch_cnt]
        query_json = {"_source": ["org_id"], "query": {"ids": {"values": batch_person_ids}}}
        query_res = es.search(index=[person_v9_index], body=query_json)
        results += query_res["hits"]["hits"]

    person_id_org_id_map = dict()
    for row in results:
        person_id = row.get("_id")
        org_id = row.get("_source", {}).get("org_id")
        person_id_org_id_map[person_id] = org_id
        fields_set = person_id_fields_map.get(person_id)
        org_logger.info(f"get person from es, person_id: {person_id}, org_id: {org_id}")
        if fields_set is None:
            org_logger.error(f"fuck person lack fields set person_id: {person_id}, fields set: {fields_set}")
            fields_set = set()
        if org_id:
            org_id_field_map[org_id] |= fields_set

    t1 = datetime.datetime.now()
    org_logger.info(f"end to get person, person_len: {len(person_ids)}, es_results: {len(results)}, person_id_org_id_map_cnt: {len(person_id_org_id_map)}  now: {t1}, cost_time: {(t1 - t0).total_seconds()}")
    return person_id_org_id_map


def update_person_org_id(person_ids: List[str], person_id_fields_map: dict, start: int, end: int):
    mongo_client = MongoClient(
        host="192.168.0.42",
        port=27017,
        username="admin",
        password="gkx_2022",
        authSource="admin",
    )
    person_final_col = mongo_client["industry_graph"]["person_final"]

    org_logger = get_logger(parent_dir=log_path, name=f"cell_and_gene_update_person_org_{start}_{end}")
    org_logger.info(f"start to complete org_id to person, start:{start}, end:{end}, now: {datetime.datetime.now()}")
    bulk_reqs = []
    org_id_field_map = defaultdict(set)
    person_id_org_id_map = dict()
    try:
        person_id_org_id_map = get_person_org_ids(person_ids=person_ids,
                                                  org_id_field_map=org_id_field_map,
                                                  person_id_fields_map=person_id_fields_map,
                                                  org_logger=org_logger,
                                                  )
    except Exception as e:
        org_logger.error(f"get person_id_org_id_map error, e: {e}")
    for person_id, org_id in person_id_org_id_map.items():
        bulk_reqs.append(UpdateOne(filter={"aminer_id": person_id}, update={"$set": {"org_id": org_id}}))
    if bulk_reqs:
        person_final_col.bulk_write(bulk_reqs)
    org_logger.info(f"end to complete org_id to person, start:{start}, end:{end}, now: {datetime.datetime.now()}")
    return org_id_field_map


def complete_org_id(input_path: str):
    if os.path.exists(input_path):
        return

    t0 = datetime.datetime.now()
    print(f"start to complete org id, now: {t0}")

    # 获取所有 paper_ids
    person_ids = []
    person_id_fields_map = defaultdict(set)

    batch_cnt = 1000
    pool = Pool(16)
    results = []

    # 获取所有 person_ids
    mongo_client = MongoClient(
        host="192.168.0.42",
        port=27017,
        username="admin",
        password="gkx_2022",
        authSource="admin",
    )
    person_final_col = mongo_client["industry_graph"]["person_final"]
    cursor = person_final_col.find({"org_id": {'$exists': False}}, ['aminer_id', "fields"]).batch_size(100)

    i_count = 0
    for row in cursor:
        person_id = row["aminer_id"]
        fields = row["fields"]
        i_count += 1
        print(f"get person_id, num: {i_count}, now: {datetime.datetime.now()}")
        person_ids.append(person_id)
        for field in fields:
            tec_field_root = field["tec_field_root"]
            tec_field_larg = field["tec_field_larg"]
            tec_field_medi = field["tec_field_medi"]
            tec_field_mini = field["tec_field_mini"]
            person_id_fields_map[person_id].add((tec_field_root, tec_field_larg, tec_field_medi, tec_field_mini))

        # if i_count >= 1000:
        #     break

    # 通过 es 补充 org_id 到 person 数据的学者数据中
    for step_index in range(len(person_ids))[::batch_cnt]:
        batch_person_ids = person_ids[step_index:step_index+batch_cnt]
        process_result = pool.apply_async(update_person_org_id, args=(batch_person_ids, person_id_fields_map, step_index, step_index+batch_cnt))
        results.append(process_result)

    pool.close()
    pool.join()

    # 合并所有 org_id_field_map
    print(f"start to merge all org_id_field_map, now: {datetime.datetime.now()}")
    all_org_id_field_map = defaultdict(set)
    for future_result in results:
        org_id_field_map = future_result.get()
        print(f"org_id_field_map, len: {len(org_id_field_map)}")
        for org_id, field_set in org_id_field_map.items():
            print(f"fuck org_id: {org_id}, field_set: {field_set}")
            if org_id not in all_org_id_field_map:
                all_org_id_field_map[org_id] = field_set
            else:
                all_org_id_field_map[org_id] |= field_set
    print(f"end to merge all org_id_field_map, now: {datetime.datetime.now()}, org_id count: {len(all_org_id_field_map)}")

    # 最后将 org_id_field_map 存到文件中
    with open(input_path, "w") as f:
        for org_id, fields_set in all_org_id_field_map.items():
            new_fields = []
            for field_tuple in fields_set:
                new_fields.append({"tec_field_root": field_tuple[0], "tec_field_larg": field_tuple[1], "tec_field_medi": field_tuple[2], "tec_field_mini": field_tuple[3]})
            f.write(json.dumps({"org_id": org_id, "fields": new_fields}, ensure_ascii=False))
            f.write("\n")

    t1 = datetime.datetime.now()
    print(f"end to complete org id, now: {t1}, cost_time: {(t1 - t0).total_seconds()}")


def generate_org_data_from_org_api(input_path: str, sz_org_path: str):
    """
    获取机构数据
    1. 首先遍历论文库和学者库的数据, 去 es 获取对应的 org_id;
    2. 根据 org_id 获取对应的 org 详情数据, 入库到 mongo
    """
    complete_org_id(input_path)
    get_org_data_by_org_ids(input_path, sz_org_path)


if __name__ == '__main__':
    import sys
    input_path = sys.argv[1]
    sz_org_path = sys.argv[2]
    log_path = sys.argv[3]
    generate_org_data_from_org_api(input_path, sz_org_path)

