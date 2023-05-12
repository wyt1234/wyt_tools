from pymongo import MongoClient

host = "117.119.77.139"
port = 30019
db_name = "eitools"
user = "xuwei"
password = "tUl1PsT*3WcUl"
authSource = "eitools"

# 创建一个MongoClient实例（这两种方法好像都可以）
client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}", directConnection=True)
client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}/?authSource={authSource}")

# 选择要连接的数据库
db = client[db_name]

# 测试连接是否成功，尝试获取数据库中的集合列表
collection_names = db.list_collection_names()
print(f"连接成功，数据库 '{db_name}' 中的集合列表：")
print(collection_names)

# 关闭连接
client.close()
