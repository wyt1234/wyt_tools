from pathlib import Path
from prettytable import PrettyTable

x = PrettyTable()
x.field_names = ["接口名称", "系统名称", "接口路径"]
x.align = "l"


def o():
    with open('aminersz使用的北京前端接口.js', 'r') as f:
        docs = f.readlines()
    return docs


def run():
    docs = o()
    for line in docs:
        # print(line)
        line = line.lstrip()
        if line.find('//') >= 0 or line.find('/*') >= 0:
            continue
        line = line.replace('`', '').replace('`', '').replace(',', '').replace('\n', '')
        name = line.split(':', 1)[0]
        other = line.split(':', 1)[1]
        url = line.split(':', 1)[1].split('}')[1]
        baseURL = other.replace(url, '').lstrip()
        if baseURL == '${baseURL}':
            baseURL = 'https://api.aminer.cn/api'
        if baseURL == '${nextAPIURLOnlineProduction}':
            baseURL = 'https://apiv2.aminer.cn'
        x.add_row([name, "Aminer", baseURL+url])
        print(baseURL, url)
    print(x)
    with open("导出Aminersz前端接口.txt", 'w', encoding='utf8') as fp:
        fp.write(x.get_string())
    return


if __name__ == '__main__':
    run()
