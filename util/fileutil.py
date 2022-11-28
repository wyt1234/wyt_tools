import json, os
import time


# from ioservice.common.celery_app import app


class FileServer:
    def __init__(self, path, init=False):
        self.path = path
        self.structure = "list"
        self.data = None
        if init:
            self.rm_exist()

    def rm_exist(self):
        if os.path.exists(self.path):
            print(f"{self.path} is exist, start to delete")
            try:
                os.remove(self.path)
                print(f"remove success")
            except Exception as e:
                print(f"{e}")

    def save_init(self):
        types = {"list": list(), "dict": dict()}
        if self.structure.lower() in types.keys():
            with open(self.path, 'w') as f:
                f.write(json.dumps(types[self.structure.lower()]))

    # @app.task
    def update(self, data, retry=0):
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                f.write(json.dumps([] if type(data) == "list" else {}, ensure_ascii=False))
        try:
            saved = json.load(open(self.path))
            if type(data) == "list":
                saved.append(data)
            elif type(data) == "dict":
                saved.update(data)
            with open(self.path, 'w') as f:
                f.write(json.dumps(saved, ensure_ascii=False))
        except Exception as e:
            print(e)
            if retry > 5:
                return
            time.sleep(1)
            self.update(data, retry + 1)


# @app.task
def update_file(path, data, retry=0):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write(json.dumps([] if type(data) == "list" else {}, ensure_ascii=False))
    try:
        saved = json.load(open(path))
        if type(data) == "list":
            saved.append(data)
        elif type(data) == "dict":
            saved.update(data)
        with open(path, 'w') as f:
            f.write(json.dumps(saved, ensure_ascii=False))
    except Exception as e:
        print(e)
        if retry > 5:
            return
        time.sleep(1)
        update_file(data, data, retry + 1)
