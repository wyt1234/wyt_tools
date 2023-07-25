import pandas as pd
import re
from tqdm import tqdm

'''https://chat.openai.com/share/e5fa642f-022b-40c4-8130-211c7bb04d0c'''
'''prompt：同一行中，“资讯段落”列中出现"重点匹配词"(按"、"隔开)的文本标颜色并加粗，并把“资讯段落”列中出现“姓名”列中出现的文本标记颜色并加粗（只标出重合的段落，注意都是连起来），导出前100行为Markdown表格，最后预留一列给我做标签'''

# Load the Excel file
df = pd.read_excel("ref2数据验证集.xlsx")

# Display the first few rows of the DataFrame
df.head()


# Define a function to add markdown to a text
def mark_text(text, mark_words, color):
    for word in mark_words:
        pattern = re.compile(f'({word})', re.IGNORECASE)
        text = pattern.sub(f'<span style="color:{color}; font-weight:bold">\\1</span>', text)
    return text


# Try to process only the first 100 rows to avoid MemoryError
df_small = df.head(500).copy()    # 前100行
# df_small = df.copy()  # TODO 全量数据

tqdm.pandas(desc="Processing")

df_small['资讯段落'] = df_small.apply(lambda row: mark_text(row['资讯段落'], row['重点匹配词'].split('、'), 'red'),
                                      axis=1)
df_small['资讯段落'] = df_small.apply(lambda row: mark_text(row['资讯段落'], [row['姓名']], 'blue'), axis=1)

#
df_small['人才库匹配简历'] = df_small.apply(
    lambda row: mark_text(row['人才库匹配简历'], row['重点匹配词'].split('、'), 'red'), axis=1)
df_small['人才库匹配简历'] = df_small.apply(lambda row: mark_text(row['人才库匹配简历'], [row['姓名']], 'blue'), axis=1)

# Add an empty column for labels
df_small['人工标签'] = ''

# Replace '|' with '/' in the DataFrame
df_small = df_small.replace('\|', '/', regex=True)

# Display the first few rows of the DataFrame
df_small.head()

# Select the columns to export
df_small = df_small[['资讯标题', '人才库匹配简历', '姓名', '资讯段落']]

# Convert the DataFrame to a markdown string
markdown_table = df_small.to_markdown(index=False)

# Save the markdown string to a file
with open('ref2数据验证集高亮.md', 'w') as file:
    file.write(markdown_table)

'ref2数据验证集高亮.md'
print(markdown_table)
