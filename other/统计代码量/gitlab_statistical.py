#!/usr/bin/python3
# coding=utf8
# @Author: Mario
# @Date  : 2020/11/04
# @Desc  : GitLab 按时间查看各用户代码提交量官方API版

import json
import requests
from dateutil.parser import parse

gitlab_url = "https://dev.aminer.cn/"  # GitLab 地址
private_token = "glpat-K237fBzFXzc3jJjSiYy_"  # GitLab Access Tokens（管理员权限）

info = []

headers = {
    'Connection': 'close',
}


# UTC时间转时间戳
def utc_time(time):
    dt = parse(time)
    return int(dt.timestamp())


# 输出格式化
def str_format(txt):
    lenTxt = len(txt)
    lenTxt_utf8 = len(txt.encode('utf-8'))
    size = int((lenTxt_utf8 - lenTxt) / 2 + lenTxt)
    length = 20 - size
    return length


# 获取 GitLab 上的所有项目
def gitlab_projects():
    project_ids = []
    page = 1
    while True:
        url = gitlab_url + "api/v4/projects/?private_token=" + private_token + "&page=" + str(page) + "&per_page=20"
        while True:
            try:
                res = requests.get(url, headers=headers, timeout=10)
                break
            except Exception as e:
                print(e)
                continue
        projects = json.loads(res.text)
        if len(projects) == 0:
            break
        else:
            for project in projects:
                project_ids.append(project["id"])
            page += 1
    return project_ids


# 获取 GitLab 上的项目 id 中的分支
def project_branches(project_id):
    branch_names = []
    page = 1
    while True:
        url = gitlab_url + "api/v4/projects/" + str(
            project_id) + "/repository/branches?private_token=" + private_token + "&page=" + str(page) + "&per_page=20"
        while True:
            try:
                res = requests.get(url, headers=headers, timeout=10)
                break
            except Exception as e:
                print(e)
                continue
        branches = json.loads(res.text)
        '''Debug
        print(url)
        print('--' * 10)
        print(branches)
        print('*' * 10)
        '''
        if len(branches) == 0:
            break
        else:
            for branch in branches:
                branch_names.append(branch["name"])
            page += 1
    return branch_names


# 获取 GitLab 上的项目分支中的 commits，当 title 或 message 首单词为 Merge 时，表示合并操作，剔除此代码量
def project_commits(project_id, branch, start_time, end_time):
    commit_ids = []
    page = 1
    while True:
        url = gitlab_url + "api/v4/projects/" + str(
            project_id) + "/repository/commits?ref_name=" + branch + "&private_token=" + private_token + "&page=" + str(
            page) + "&per_page=20"
        while True:
            try:
                res = requests.get(url, headers=headers, timeout=10)
                break
            except Exception as e:
                print(e)
                continue
        commits = json.loads(res.text)
        if len(commits) == 0:
            break
        else:
            for commit in commits:
                if "Merge" in commit["title"] or "Merge" in commit["message"] or "合并" in commit["title"] or "合并" in \
                        commit["message"]:  # 不统计合并操作
                    continue
                elif utc_time(commit["authored_date"]) < utc_time(start_time) or utc_time(
                        commit["authored_date"]) > utc_time(end_time):  # 不满足时间区间
                    continue
                else:
                    commit_ids.append(commit["id"])
            page += 1
    return commit_ids


# 根据 commits 的 id 获取代码量
def commit_code(project_id, commit_id):
    global info
    url = gitlab_url + "api/v4/projects/" + str(
        project_id) + "/repository/commits/" + commit_id + "?private_token=" + private_token
    while True:
        try:
            res = requests.get(url, headers=headers, timeout=10)
            break
        except Exception as e:
            print(e)
            continue
    data = json.loads(res.text)
    temp = {"name": data["author_name"], "additions": data["stats"]["additions"],
            "deletions": data["stats"]["deletions"], "total": data["stats"]["total"]}  # Git工具用户名,新增代码数,删除代码数,总计代码数
    info.append(temp)


# GitLab 数据查询
def gitlab_info(start_time, end_time):
    for project_id in gitlab_projects():  # 遍历所有项目ID
        for branche_name in project_branches(project_id):  # 遍历每个项目中的分支
            for commit_id in project_commits(project_id, branche_name, start_time, end_time):  # 遍历每个分支中的 commit id
                commit_code(project_id, commit_id)  # 获取代码提交量


if __name__ == "__main__":
    print("正在统计数据，请耐心等待，这将花费不少时间~")
    gitlab_info('2023-01-01 00:00:00', '2023-12-31 23:59:59')  # 起-止时间
    name = []  # Git工具用户名
    additions = []  # 新增代码数
    deletions = []  # 删除代码数
    total = []  # 总计代码数
    res = {}

    # 生成元组
    for i in info:
        for key, value in i.items():
            if key == "name":
                name.append(value)
            if key == "additions":
                additions.append(value)
            if key == "deletions":
                deletions.append(value)
            if key == "total":
                total.append(value)
    data = list(zip(name, additions, deletions, total))
    # print(data)
    # 去重累加
    for j in data:
        name = j[0]
        additions = j[1]
        deletions = j[2]
        total = j[3]
        if name in res.keys():
            res[name][0] += additions
            res[name][1] += deletions
            res[name][2] += total
        else:
            res.update({name: [additions, deletions, total]})

    # 打印结果
    print("Git用户名           新增代码数           删除代码数            总计代码数")
    for k in res.keys():
        print(k + " " * str_format(k) + str(res[k][0]) + " " * str_format(str(res[k][0])) + str(
            res[k][1]) + " " * str_format(str(res[k][1])) + str(res[k][2]))
