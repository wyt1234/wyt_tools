import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
import pandas as pd
import re
from tqdm import tqdm
import gc

'''highlighted_table提速版'''

# Load the Excel file
df = pd.read_excel("ref2数据验证集.xlsx", nrows=250)


# Define a function to add markdown to a text
def mark_text(row, column):
    mark_words = row['重点匹配词'].split('、') + [row['姓名']]
    colors = ['red'] * len(row['重点匹配词'].split('、')) + ['blue']
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

# Select the columns to export
df_result = df_result[['序号', '资讯标题', '人才库匹配简历', '姓名', '资讯段落', '人工标签']]

# Convert the DataFrame to an HTML string
html_string = df_result.to_html(escape=False, index=False, render_links=True)

# Add a <meta> tag to specify the encoding
html_string = '<meta charset="UTF-8">\n' + html_string

# Save the HTML string to a file
with open('ref2数据验证集高亮.html', 'w', encoding='utf-8') as file:
    file.write(html_string)
