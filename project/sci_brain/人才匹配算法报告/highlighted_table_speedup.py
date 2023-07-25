import pandas as pd
import re
from tqdm import tqdm

# Load the Excel file
df = pd.read_excel("ref2数据验证集.xlsx")

# Define a function to add markdown to a text
def mark_text(row, column):
    mark_words = row['重点匹配词'].split('、') + [row['姓名']]
    colors = ['red'] * len(row['重点匹配词'].split('、')) + ['blue']
    text = row[column]
    for word, color in zip(mark_words, colors):
        pattern = re.compile(f'({word})', re.IGNORECASE)
        text = pattern.sub(f'<span style="color:{color}; font-weight:bold">\\1</span>', text)
    return text

# Try to process only the first 100 rows to avoid MemoryError
df_small = df.head(500).copy()    # 前100行
# df_small = df.copy()  # TODO 全量数据

# Apply the function to the DataFrame with a progress bar
tqdm.pandas(desc="Processing")
df_small['资讯段落'] = df_small.progress_apply(lambda row: mark_text(row, '资讯段落'), axis=1)
df_small['人才库匹配简历'] = df_small.progress_apply(lambda row: mark_text(row, '人才库匹配简历'), axis=1)

# Replace '|' with '/' in the DataFrame
df_small = df_small.replace('\|', '/', regex=True)

# Select the columns to export
df_small = df_small[['资讯标题', '人才库匹配简历', '姓名', '资讯段落']]

# Convert the DataFrame to a markdown string
markdown_table = df_small.to_markdown(index=False)

# Save the markdown string to a file
with open('ref2数据验证集高亮.md', 'w') as file:
    file.write(markdown_table)

print(markdown_table)
