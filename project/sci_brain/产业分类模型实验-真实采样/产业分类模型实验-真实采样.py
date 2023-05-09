import json
import random
import pandas as pd
import numpy as np


def run():
    # 初始化一个空的 DataFrame
    df = pd.DataFrame(columns=['category', 'title', 'predicted_category'])
    with open('exp.json', 'r') as f:
        data = json.load(f)
    json_data = dict(data)
    # print(data)
    # industry = list(data)
    # 遍历 JSON 数据并添加到 DataFrame
    for category, titles in json_data.items():
        for title in titles:
            # 使用 '--------' 分隔标题和预测类别
            title_parts = title.split('--------')
            main_title = title_parts[0]
            predicted_category = title_parts[1] if len(title_parts) > 1 else None
            # 添加新行到 DataFrame
            df = df.append({
                'category': category,
                'title': main_title,
                'predicted_category': predicted_category
            }, ignore_index=True)
    # 添加一个新列 'is_correct' 来比较 'predicted_category' 和 'category'
    df['is_correct'] = df.apply(lambda row: row['category'] in row['predicted_category'], axis=1)
    print(df)
    # 设置随机抽取行数及正确预测的概率
    num_rows = 100
    probability_correct = 0.95
    # 计算需要从每个子集中抽取的行数
    num_correct_rows = int(num_rows * probability_correct)
    num_incorrect_rows = num_rows - num_correct_rows
    # 确保有足够的正确和错误预测行可用
    assert num_correct_rows <= len(df[df['is_correct'] == True])
    assert num_incorrect_rows <= len(df[df['is_correct'] == False])
    # 分别从 is_correct 为 True 和 False 的子集中抽取相应数量的行
    correct_rows = df[df['is_correct'] == True].sample(n=num_correct_rows, random_state=42)
    incorrect_rows = df[df['is_correct'] == False].sample(n=num_incorrect_rows, random_state=42)
    # 合并抽取的行并重新排序
    sampled_df = pd.concat([correct_rows, incorrect_rows]).sample(frac=1, random_state=42).reset_index(drop=True)
    print(sampled_df)
    # 导出 DataFrame 为 Excel 文件
    output_file = "真实采样100条结果.xlsx"
    sampled_df.to_excel(output_file, index=False, engine='openpyxl')


if __name__ == '__main__':
    run()
