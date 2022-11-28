# coding=utf-8
import sys
import time

sys.path.append("..")
from bs4 import BeautifulSoup
from summa.summarizer import summarize
from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor
from loguru import logger
import json
import os
import sys
import requests
import Levenshtein

pubs_pool = ThreadPoolExecutor(5)
session = HTMLSession()

end_lists_doc = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs/end_words.json')))


def get_abstract(url):
    try:
        r = session.get(url)
    except Exception as e:
        exc_type, exc_value, exc_obj = sys.exc_info()
        logger.error("exception_type: %s,exception_value: %s,exception_object: %s," % (
            str(exc_type), str(exc_value), str(exc_obj)))
        return "", ""
    a = r.html.text.split('\n')  # r.html.text可去掉html中的所有标签
    flag = False  # 使用flag来确定是否为需写入的内容
    lists = ['来源：', '阅读原文', '喜欢本篇内容', '分享、点赞', '原文链接', '收录于话题', '点击上方', '微信平台', '发自', '公众号',
             '点击下方', '点击直达', '长按识别', '👇', '扫描下方', '本期贡献者', '二维码', '作者', '责编', '记者', "联系邮箱"]
    alllist = []
    allstr = ""
    title_list = get_inbound_link_title(r.html.links)
    # title_list=[]
    for num in range(len(a)):
        if '功能介绍' in a[num]:  # 写入‘功能介绍’以后的内容
            flag = True
            continue
        elif 'var first_sceen__time' in a[num]:  # 写入‘var first_sceen__time’以前的内容
            flag = False
        elif flag:
            if any(i in a[num] for i in lists):
                continue
            if a[num] == '':
                continue
            # 删除外链
            del_inbound_flag = False
            for title in title_list:
                ratio = Levenshtein.ratio(title, a[num])
                if ratio > 0.8:
                    del_inbound_flag = True
                    break
            if del_inbound_flag:
                continue
            alllist.append(a[num])
    end_words = ["投稿模板", "相关阅读", "阅读原文", "还喜欢", "写在最后", "相关进展", "参考资料", "来源", "编辑", "客服", "往期精彩", "社会责任之声", "由青年唱响全球",
                 "在看", "素材", "投稿", "网站", "分享", "关注", "联系", "感谢", "限时优惠", "订阅点击", "联系人", "微信群", "扫一扫", "来源", "回顾", "文/",
                 "图/", "猜你喜欢"]
    end_lists = {word: 0.1 for word in end_words}

    for end_word, weight in end_lists_doc.items():
        if weight > 0.1:
            end_lists[end_word] = weight
        else:
            end_lists[end_word] = 0.1
    # end_lists = {"相关进展": 1, "写在最后": 1, "还喜欢": 1, "阅读原文": 1, "相关阅读": 1, "投稿模板": 1}
    total_length = len("".join(alllist))
    now_length = 0
    for i in range(len(alllist)):
        paragraph = alllist[i]
        in_end = [word in paragraph for word in end_lists.keys()]
        if any(in_end):
            end_word = list(end_lists.keys())[in_end.index(True)]
            if len("".join(alllist[i:])) / total_length < end_lists[end_word]:
                # print(end_word, len("".join(alllist[i:])) / total_length)
                now_length += 1
                break
        allstr += paragraph + '\n'

    text = allstr

    content = summarize(text, ratio=0.3, split=False)

    try:
        if alllist[0] not in content:
            content = alllist[0] + '\n' + content
    except:
        pass
    abstract = ''.join(content)
    return abstract, text


# 获取外链的anchor，这里使用title代替anchor
def get_inbound_link_title(link):
    title_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    for i, net_link in enumerate(link):
        # print(net_link)
        html = requests.get(net_link, headers=headers, timeout=3).text
        soup = BeautifulSoup(html, 'html.parser')
        # print(result)
        og_title = soup.find("meta", property="og:title")
        if og_title != None:
            title = og_title['content']
            title_list.append(title)
    return title_list


if __name__ == "__main__":
    pass
    start = time.time()
    abstract, content = get_abstract("https://blog.csdn.net/weixin_41894030/article/details/115264687")
    # print(abstract)
    print(" ".join(content.split()))
    print(time.time() - start)
