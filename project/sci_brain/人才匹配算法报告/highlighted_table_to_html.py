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

# Add a title to the HTML file and table border
html_string = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>“大模型+正则”人才匹配方法</title>
    <style>
        h1 {text-align: center;}
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
<h1>“大模型+正则”人才匹配方法</h1>
''' + df_result.to_html(escape=False, index=False) + '</body>\n</html>'

# Save the HTML string to a file
with open('ref2数据验证集高亮.html', 'w', encoding='utf-8') as file:
    file.write(html_string)
