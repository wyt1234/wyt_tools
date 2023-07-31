import sys
import io
import pandas as pd
import re
from tqdm import tqdm
import gc

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

'''highlighted_table提速版'''

# Load the Excel file
df = pd.read_excel("ref2数据验证集.xlsx", nrows=250)


# Define a function to add markdown to a text
def mark_text(row, column):
    # split and remove empty strings
    mark_words = [word for word in row['重点匹配词'].split('、') if word] + [row['姓名']]
    colors = ['red'] * len([word for word in row['重点匹配词'].split('、') if word]) + ['blue']
    text = row[column]
    for word, color in zip(mark_words, colors):
        pattern = re.compile(f'({word})', re.IGNORECASE)
        text = pattern.sub(f'<span style="color:{color}; font-weight:bold">\\1</span>', text)
    gc.collect()  # Manually collect garbage after processing each row
    return text


# Define batch size
batch_size = 100

# Initialize an empty DataFrame to store the results
df_result = pd.DataFrame()

# Process the data in batches
for i in tqdm(range(0, len(df), batch_size), desc="Processing"):
    df_batch = df.iloc[i:i + batch_size].copy()
    df_batch['资讯段落'] = df_batch.apply(lambda row: mark_text(row, '资讯段落'), axis=1)
    df_batch['人才库匹配简历'] = df_batch.apply(lambda row: mark_text(row, '人才库匹配简历'), axis=1)
    df_result = pd.concat([df_result, df_batch])

# Add an empty column for labels
df_result['人工标签'] = 1

# Replace '|' with '/' in the DataFrame
df_result = df_result.replace('\|', '/', regex=True)

# Add a new column with a sequence of integers starting from 1
df_result.insert(0, '序号', range(1, 1 + len(df_result)))

'''手工标注的标签'''
# Add an empty column for labels
df_result['人工标签'] = '正确✔'

# Modify the '人工标签' column for specific rows
df_result.loc[[25, 26, 45, 55, 62, 98, 142, 152, 160, 162, 165, 166, 168, 174, 175, 187, 247], '人工标签'] = '错误×'
df_result.loc[[14, 43, 61, 67, 96, 111, 112, 114, 116, 130, 163, 182, 183, 188, 203, 216, 217, 226, 230, 231,
               242], '人工标签'] = '无法判断'

# Select the columns to export
df_result = df_result[['序号', '资讯标题', '人才库匹配简历', '姓名', '资讯段落', '人工标签']]

# Set the column widths
df_result_styled = df_result.style.set_table_styles([
    {'selector': 'th', 'props': [('width', '20%')]},  # Set the width of the header cells
    {'selector': 'td', 'props': [('width', '20%')]},  # Set the width of the data cells
])


report_string = '''
<p>1. 概述</p>
<p>本报告总结了我们对人才信息抽取和匹配算法的改进。原始算法主要通过抽取资讯原文中的人名和人才上下文，然后在Aminer中查询人才知识库，并结合语义进行判断。新的改进方法在原有基础上，增加了使用ChatGLM2大模型和正则匹配的步骤，提高了算法的准确性和精确性。</p>
<p>2. 改进方法</p>
<p>新的改进方法包括以下步骤：</p>
<p>资讯机构提示：基于资讯内容，构建对话模型的输入。</p>
<p>人才简历提示：从Aminer中获取人才的详细信息，构建对话模型的输入。</p>
<p>正则匹配验证：使用ChatGLM2模型获取模型的输出，这些输出主要是人才在资讯中的机构和简历中的机构，然后比较资讯中的机构和简历中的机构，看是否匹配。</p>
<p>生成推荐解释和证据：根据匹配结果，生成推荐解释和证据。</p>
<p>（流程图）</p>
<p>3. 改进效果</p>
<p>新的改进方法显著提高了算法的准确性和精确性。特别是对于常见姓名（如张丹、王峰、徐凯、王华等），原先的方法容易出错，而新的方法通过机构匹配，基本解决了这个问题。此外，新的方法在一定程度上避免了非重点人员出现的情况，通过新的方法，我们能够更准确地抽取和匹配到重点人员。</p>
<p>4. 性能指标</p>
<p>新的改进方法在各项性能指标上都有显著提升。具体的性能指标对比如下：</p>
'''

table_string = '''
<table>
    <tr>
        <th>指标</th>
        <th>原方法</th>
        <th>新方法</th>
        <th>最大提升比</th>
    </tr>
    <tr>
        <td>精确率</td>
        <td>54.17%</td>
        <td>93.20%</td>
        <td><strong>71.98%</strong></td>
    </tr>
    <tr>
        <td>准确率</td>
        <td>54.17%</td>
        <td>84.52%</td>
        <td><strong>55.97%</strong></td>
    </tr>
    <tr>
        <td>召回率</td>
        <td>-</td>
        <td>79.25%</td>
        <td>-</td>
    </tr>
    <tr>
        <td>F1分数</td>
        <td>-</td>
        <td>85.62%</td>
        <td>-</td>
    </tr>
</table>
'''

conclusion_string = '''
<p>5. 结论</p>
<p>新的改进方法显著提高了人才信息抽取和匹配算法的性能，特别是在处理常见姓名和非重点人员的情况时，表现出了显著的优势。</p>
<p>另：统计了89万篇资讯，有收录专家出现的几率约5.3%（公众号，定向）。</p>
<p>6.数据集</p>
'''


html_string = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>"大模型+正则"人才匹配算法</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        h2 {
            color: #666;
        }
        p {
            text-indent: 2em;
            line-height: 1.6;
            color: #333;
        }
        table {
            border-collapse: collapse;
            width: 100%; /* Make the table width 100% of its container */
        }
        th, td {
            border: 1px solid black;
            text-align: center; /* Center the text in header cells */
            overflow-wrap: anywhere; /* This will allow words to break and wrap onto the next line */
        }
        /* Set the widths of the table cells based on their content */
        th:nth-child(1), td:nth-child(1) {
            width: 5%;
        }
        th:nth-child(2), td:nth-child(2) {
            width: 15%;
        }
        th:nth-child(3), td:nth-child(3) {
            width: 40%;
        }
        th:nth-child(4), td:nth-child(4) {
            width: 5%;
        }
        th:nth-child(5), td:nth-child(5) {
            width: 30%;
        }
        th:nth-child(6), td:nth-child(6) {
            width: 5%;
        }
    </style>
</head>
<body>
<h1>"大模型+正则"人才匹配算法</h1>
''' + report_string + table_string + conclusion_string + df_result.to_html(escape=False, index=False) + '</body>\n</html>'

# Save the HTML string to a file
with open('ref2数据验证集高亮.html', 'w', encoding='utf-8') as file:
    file.write(html_string)
