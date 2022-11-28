from difflib import SequenceMatcher

'''内置函数、'''
if __name__ == '__main__':
    checking = SequenceMatcher(None, '我是啊啊啊', '你是啊啊').ratio()
    checking = SequenceMatcher(None, '你是啊啊', '我是啊啊啊').ratio()
    print(f"文本相似度为{checking * 100} % similar")
