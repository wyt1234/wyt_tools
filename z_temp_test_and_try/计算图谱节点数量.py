import json
import os

import requests
from tqdm import tqdm


def expert(id):
    url = "https://kd.top3-talent.com/api/graph/related"
    payload = json.dumps({
        "id": f"{id}",
        "type": "expert",
        "offset": 0,
        "size": 12
    })
    headers = {
        'Content-Type': 'application/json'
    }
    requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
    s = requests.sessions.Session()
    s.keep_alive = False  # 关闭多余的连接
    response = s.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    try:
        return response.json()['data']['expert_count']
    except Exception as e:
        print(e)
        return 0


def paper(id):
    url = "https://kd.top3-talent.com/api/graph/related"
    payload = json.dumps({
        "id": f"{id}",
        "type": "paper",
        "offset": 0,
        "size": 12
    })
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json'
    }
    requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
    s = requests.sessions.Session()
    s.keep_alive = False  # 关闭多余的连接
    response = s.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    try:
        return response.json()['data']['paper_count']
    except Exception as e:
        print(e)
        return 0


node_map = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'node_map.json')))
print(len(node_map))
a = len(node_map)
for node in tqdm(node_map):
    n = node_map[node]
    id = n['id']
    try:
        e = expert(id)
        p = paper(id)
        a += e
        a += p
        print(f'总数为：{a}')
    except Exception as e:
        print('kill')
