from hashlib import md5

import redis

from loguru import logger
from xwtools.config_log import config


class RedisDB:

    def __init__(self):
        conf_str = 'redis_localhost'
        logger.info('获取redis实例：{}', conf_str)
        host = config(conf_str, 'host')
        password = config(conf_str, 'pass')

        self.__pool = redis.ConnectionPool(host=host, password=password)  # redis默认端口是6379
        self._redis = redis.Redis(connection_pool=self.__pool)

    # 集合操作
    def sadd(self, key, val):
        return self._redis.sadd(key, val)

    def getbit(self, name, loc):
        return self._redis.getbit(name, loc)

    def setbit(self, name, loc):
        return self._redis.setbit(name, loc, 1)

    def sysmenber(self, key, val):
        return self._redis.sismember(key, val)

    def __del__(self):
        self._redis.close()


redis_client = RedisDB()


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed
        # self.seeds = [5, 7, 11, 13, 31, 37, 61]

    def hash(self, value):
        ret = 0
        # print(value)
        for i in range(len(value)):
            # print('>>', ret, self.seed, value[i])
            ret += self.seed * ret + ord(value[i])
        # print('cap:', self.cap, ret,  (self.cap - 1) & ret)
        return (self.cap - 1) & ret


class BloomFilter(object):
    def __init__(self, blockNum=1, key='bloomfilter'):
        """
        :param host: the host of Redis
        :param port: the port of Redis
        :param db: witch db in Redis
        :param blockNum: one blockNum for about 93,000,000; if you have more strings for filtering, increase it.
        :param key: the key's name in Redis
        """
        self.server = redis_client
        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def hash_md5(self, str_input):
        m5 = md5()
        str_input = str_input.encode("utf-8")
        m5.update(str_input)
        return m5.hexdigest()

    def redis_key(self, str_input):
        return self.key + str(int(str_input[0:2], 16) % self.blockNum)

    def isContains(self, str_input):
        str_md5 = self.hash_md5(str_input)
        # ret 在计算过程中是 0 | 1
        ret = 1
        # redis的key 前缀
        name = self.redis_key(str_md5)
        for f in self.hashfunc:
            # loc 为 hash 之后得到的二进制哈希数值
            loc = f.hash(str_md5)
            ret = ret & self.server.getbit(name, loc)
            # print('getbit: ', name, loc, ret)
        return ret

    def insert(self, str_input):
        str_md5 = self.hash_md5(str_input)
        name = self.redis_key(str_md5)
        for f in self.hashfunc:
            loc = f.hash(str_md5)
            self.server.setbit(name, loc)


if __name__ == '__main__':
    bf = BloomFilter()
    strs = 'http://www.baidu.com'
    # strs = '123'
    if bf.isContains(strs):  # 判断字符串是否存在
        print('exists!')
    else:
        print('not exists!')
        bf.insert('http://www.baidu.com')
