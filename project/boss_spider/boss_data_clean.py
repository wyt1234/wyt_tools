import os
import re

import pandas as pd
from pathlib import Path
from tqdm import tqdm
import datetime
from loguru import logger


def info(msg):
    logger.info(msg)


# 企业简称表
def short_name_table():
    dir = 'input/名单对应企业简称.xlsx'
    df = pd.read_excel(dir)
    return df


df_short_name = short_name_table()
key_word_dict = {
    row.简称: row.全称
    for row in df_short_name.itertuples()
}


def merge_func(row):
    # 新增一列，表示能匹配的keyids
    row["keyids"] = [
        keyid
        for key_word, keyid in key_word_dict.items()
        if re.search(key_word, row["企业全称"], re.IGNORECASE)
    ]
    return row


def read_and_concat() -> pd.DataFrame:
    dirs = ['input']
    all_files = []
    for dir in dirs:
        path_list = [p for p in Path(dir).glob('2023-*.xlsx')]
        all_files.extend(path_list)
    dflist = []
    for fi in tqdm(all_files[:], '正在读取文件：'):
        # df = pd.read_excel(fi, sheet_name='模板表', usecols=cols)
        df = pd.read_excel(fi)
        dflist.append(df)
    info('正在合并文件')
    df_combine = pd.concat(dflist)  # 合并
    df = df_combine
    return df


def run():
    df = read_and_concat()
    # 公司字段非空
    df = df[~df['字段1'].isna()]
    # 共有多少岗位在招聘
    df_sum = df.groupby(['字段1']).size().reset_index().rename(columns={0: '共有多少岗位在招聘'})  # 共有多少岗位在招聘
    df = df.merge(df_sum, how='left', left_on='字段1', right_on='字段1')
    # 筛选学历
    df = df[df['tag-list2'].str.contains('硕士') | df['tag-list2'].str.contains('博士') | df['详情标题'].str.contains('博士')]
    # 共有多少研究型岗位在招聘
    df_sum = df.groupby(['字段1']).size().reset_index().rename(columns={0: '共有多少研究型岗位在招聘'})  # 共有多少岗位在招聘
    df = df.merge(df_sum, how='left', left_on='字段1', right_on='字段1')
    # 研究型岗位比例
    df['研究型人才相关岗位比例'] = df['共有多少研究型岗位在招聘'] / df['共有多少岗位在招聘']
    #
    df['岗位名称'] = df['标题']
    # df['岗位标签1'] = df['tag-list']
    # df['研究型标签'] = df['tag-list3'].str.cat([df['tag-list4'], df['tag-list5'], df['tag-list6']], sep='、')
    df['研究型标签'] = df['字段12']
    df['JD'] = df['详情标题']
    df['企业全称'] = df['字段1']
    df['企业简称'] = df['字段7']
    df['地址'] = df['字段6']
    df['BOSS链接'] = df['标题链接']
    df['薪资'] = df['salary']
    df['学历'] = df['tag-list2']
    df['工作经验'] = df['tag-list1']
    # 模糊匹配给定范围的企业
    df_merge = df.apply(merge_func, axis=1)
    df_merge.explode("keyids")
    df = pd.merge(
        # how='left',
        left=df_merge.explode("keyids"),
        right=df_short_name,
        left_on="keyids",
        right_on="全称"
    )
    df['匹配到给定范围内企业'] = df['全称']
    # 筛选深圳
    df_only_shenzhen = df[
        df.select_dtypes(include=[object]).applymap(lambda x: '深圳' in x if pd.notnull(x) else False).any(axis=1)]
    columns = ['匹配到给定范围内企业', '岗位名称', '研究型标签', '共有多少岗位在招聘', '共有多少研究型岗位在招聘', '研究型人才相关岗位比例', 'JD', '地址', 'BOSS链接', '薪资',
               '学历', '工作经验', '企业全称']
    save_path = 'output'
    with pd.ExcelWriter(os.path.join(save_path, '100家匹配结果.xlsx'), engine='xlsxwriter') as writer:
        df_only_shenzhen.to_excel(writer, '100家匹配结果（深圳内）', columns=columns, index=False)
        df.to_excel(writer, '100家匹配结果（全国）', columns=columns, index=False)
        writer.save()
    info('导出完成')
    return


if __name__ == '__main__':
    run()
