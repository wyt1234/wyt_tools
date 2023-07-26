import pandas as pd
import re
from tqdm import tqdm

# Load the Excel file
df = pd.read_excel("ref2数据验证集.xlsx")


# Define a function to add markdown to a text
def mark_text(text, mark_words, color):
    for word in mark_words:
        if word:  # Only apply markdown if the word is not empty
            pattern = re.compile(f'({word})', re.IGNORECASE)
            text = pattern.sub(f'<span style="color:{color}; font-weight:bold">\\1</span>', text)
    return text


# Try to process only the first 100 rows to avoid MemoryError
df_small = df.head(300).copy()  # 前100行

df_small['资讯段落'] = df_small.apply(
    lambda row: mark_text(row['资讯段落'], row['重点匹配词'].split('、') if row['重点匹配词'] else [], 'red'), axis=1)
df_small['资讯段落'] = df_small.apply(lambda row: mark_text(row['资讯段落'], [row['姓名']], 'blue'), axis=1)

df_small['人才库匹配简历'] = df_small.apply(
    lambda row: mark_text(row['人才库匹配简历'], row['重点匹配词'].split('、') if row['重点匹配词'] else [], 'red'),
    axis=1)
df_small['人才库匹配简历'] = df_small.apply(lambda row: mark_text(row['人才库匹配简历'], [row['姓名']], 'blue'), axis=1)

# Add an empty column for labels
df_small['人工标签'] = 1

# Replace '|' with '/' in the DataFrame
df_small = df_small.replace('\|', '/', regex=True)

# Strip leading and trailing whitespace from all string type columns
df_small = df_small.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Add a new column with a sequence of integers starting from 1
df_small.insert(0, '序号', range(1, 1 + len(df_small)))

# Select the columns to export
df_small = df_small[['序号', '资讯标题', '人才库匹配简历', '姓名', '资讯段落', '人工标签']]

# Convert the DataFrame to a markdown string
markdown_table = df_small.to_markdown(index=False)

# Use regex to remove unnecessary spaces
markdown_table_no_spaces = re.sub(' +\|', '|', markdown_table)
markdown_table_no_spaces = re.sub('\| +', '|', markdown_table_no_spaces)

# Save the markdown string to a file
with open('ref2数据验证集高亮.md', 'w') as file:
    file.write(markdown_table_no_spaces)

'ref2数据验证集高亮.md'
print(markdown_table_no_spaces)
