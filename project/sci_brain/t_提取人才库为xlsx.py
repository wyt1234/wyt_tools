import requests
import json
import pandas as pd


def fetch():
    url = "https://api.aminersz.cn/talentapi/eb/v1/manage/search/ebs"

    payload = json.dumps({
        "query": ""
    })
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Authorization': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhaWQiOiI2MmIyN2E4MDM0Yzk3ZDVmZmJkNzMwMmMiLCJhdWQiOlsiYmI0OTk5ZDUtNmExMC00OTFmLWEzMzctZGIwNjdlYjFlN2Y3Il0sImNpZCI6ImJiNDk5OWQ1LTZhMTAtNDkxZi1hMzM3LWRiMDY3ZWIxZTdmNyIsImV4cCI6MTY4MDU4NDgzMCwiZmFtaWx5X25hbWUiOiIiLCJnZW5kZXIiOjAsImdpdmVuX25hbWUiOiIiLCJpYXQiOjE2ODA1ODEyMzAsImlkIjoiNjJiMjdhODAzNGM5N2Q1ZmZiZDczMDJjIiwiaXNzIjoib2F1dGguYW1pbmVyLmNuIiwianRpIjoiZjE4N2ZmNmYtMmE5Mi00MTI4LThlMjctNGMxMDQzOTBmZWIxIiwibmJmIjoxNjgwNTgxMjMwLCJuaWNrbmFtZSI6IuWwj-mZtiIsInN1YiI6IjYyYjI3YTgwMzRjOTdkNWZmYmQ3MzAyYyIsInQiOiJQYXNzd29yZCJ9.X1lDXmfvkb54SPR6mTPiDM8keRkobDwj4XHuNJQgvulkEsiopw__OLSbtZImSFyKJkZYfytd_adhrELsiow7-yTkrmByKWksHB0x6K4xsopzf1wD6NWXd3RNRxEoE670MyUYgbCh1yrAJbTZiDmw4eat1JuFBd5CdsXyCBcH3AMVKmTXT_s3x3kxyr6pJ5IpCBZb5sv6t_I5aW1wQ-tEBqHr7m9FaoLQA8KAGITwixRgsaYqW0wJMgQlvg9jpDBdWioJnpuPF4XXPo8JLW8JwCzsGzn4-9U9FeeRc7qHrReR_9ABLXo86iY2UnKA2nFmI833Hew9HRbI37P7zNGEuA',
        'x-talent-saas': 'op',
        'Origin': 'https://aminersz.cn',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.json()


def find_children(j, res_list, lv, root):
    for item2 in j:
        item = item2.copy()
        parents = item.get('parents')
        if not parents:
            continue
        if root['id'] == parents[0]:
            item['lv'] = lv + 1
            res_list.append(item)
            find_children(j, res_list, item['lv'], item)
    return


def run():
    j = fetch()['data']
    res_list = []
    for item in j:
        parents = item.get('parents')
        if parents:
            continue
        item['lv'] = 1
        res_list.append(item)
        find_children(j, res_list, 1, item)
    # print(res_list)
    # 导出到xlsx
    xlsx_list = []
    for item in res_list:
        xlsx_item = {}
        xlsx_item['层级' + str(item['lv'])] = item.get('name_zh') or item.get('name') or ''
        xlsx_item['专家数'] = item['expert_num']
        xlsx_list.append(xlsx_item)
    pd.DataFrame(xlsx_list).to_excel('导出人才库为excel格式.xlsx', index=False)


if __name__ == '__main__':
    run()
