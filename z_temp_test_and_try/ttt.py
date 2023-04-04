



from difflib import SequenceMatcher

checking = SequenceMatcher(None, '我是啊啊啊', '你是啊啊').ratio()
print(f"文本相似度为{checking * 100} % similar")

#
# d = {1: 2, 3: 4}
# z = d.values()
# pass
# for x in d.values():
#     print(x)

# import pymilvus


# import ujson
#
#
# def aaa(a, *, c):
#     print(1)
#
#
# aaa(1, c=2)
