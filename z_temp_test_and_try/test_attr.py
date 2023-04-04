# 模拟argparser记录一下属性值的工具类
class par:
    def __init__(self):
        pass

    # def __int__(self, **kwargs):
    #     # object.__setattr__(self, 'item_dic', {})
    #     # self.item_dic = kwargs
    #     pass
    #
    # def __getattribute__(self, item):
    #     # return self.__dict__[item]
    #     return object.__getattribute__(self.item)
    #
    # def __setattr__(self, key, value):
    #     # self.item_dic[key] = value
    #     # 因为子类重写父类方法，所以要返回父类该方法完成在__dict__的注册，父类的__setattr__本质上是完成了·self.__dict__[key] = value·
    #     return object.__setattr__(self, key, value)
    #     # self.__dict__[key] = value



a = par()
a.zzz = 111
print(a.zzz)
