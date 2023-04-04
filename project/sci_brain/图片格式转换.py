from PIL import Image
from pathlib import Path


def run():
    input_dir = '/Users/wyt/Downloads/产业资讯配图'
    output_dir = '/Users/wyt/dataset/industry_default_picture'
    p_list = Path(input_dir).rglob('*')
    for p in p_list:
        if p.is_dir():
            continue
        if p.name == '.DS_Store':
            continue
        im = Image.open(p)
        name = p.name.split('.')[0] + '.jpg'
        o = Path(output_dir) / (p.parent.name + name)
        im = im.convert('RGB')
        im.save(o)
        pass


if __name__ == '__main__':
    run()
