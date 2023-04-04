import urllib.parse

url_s = '%E6%B7%B1%E5%9C%B3%E8%B6%85%E8%84%91'    # URL中被编码的部分
s = url_s.replace('%',r'\x')
b = eval('b' + '\'' + s + '\'')    # 注意这里都是单引号
# print(s)
# print(b)
# print(type(s))
# print(type(b))
print(b.decode('utf-8'))


import urllib

print(urllib.parse.quote("深圳超脑"))


