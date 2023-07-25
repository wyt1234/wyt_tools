import pandas as pd
import io
import re

# Read the markdown file
with open('ref2数据验证集高亮.md', 'r') as file:
    markdown_table = file.read()

# Split the markdown table into lines
lines = markdown_table.split('\n')

# Remove the line with the column widths
del lines[1]

# Join the lines back into a string
markdown_table = '\n'.join(lines)

# Read the markdown table into a DataFrame
df = pd.read_csv(io.StringIO(markdown_table), sep='|', skipinitialspace=True)

# Remove any empty columns
df = df.dropna(how='all', axis=1)

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# Define a function to remove HTML tags
def remove_html_tags(text):
    return re.sub('<.*?>', '', str(text))

# Remove HTML tags from the '资讯段落' and '人才库匹配简历' columns
df['资讯段落'] = df['资讯段落'].apply(remove_html_tags)
df['人才库匹配简历'] = df['人才库匹配简历'].apply(remove_html_tags)

# Display the DataFrame
print(df)
