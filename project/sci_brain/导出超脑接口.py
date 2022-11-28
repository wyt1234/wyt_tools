from pathlib import Path
from prettytable import PrettyTable

x = PrettyTable()
x.field_names = ["apiname", "method"]
x.align = "l"


def run(url):
    p_list = Path(url).rglob("*.go")
    for p in p_list:
        p_str = p.read_text()
        for line in p_str.split('\n'):
            if line.find('brainGroup.') >= 0:
                route_str = line.split('"/')[1].split('"')[0]
                route_str = 'https://www.sci-brain.cn/sci_brain/' + route_str
                route_type = line.split("brainGroup.")[1].split('(')[0]
                # print(route_str, ',', route_type)
                x.add_row([route_str, route_type])
    print(x)
    with open("接口导出.txt", 'w', encoding='utf8') as fp:
        fp.write(x.get_string())


if __name__ == '__main__':
    run('/Users/wyt/ARepo/brain_api/web/router')
