import redis


class redis_helper_class:
    def __init__(self, host='localhost', password='', port=6379, db=0):
        # 读取配置
        # redis实例
        self.r = redis.Redis(host=host, password=password, port=port, db=db, decode_responses=True)
        self._redis = self.r

    # zset index -> item_list:{'key1',99,'key2':0}
    def update_zset_index(self, index_key, item_list, ttl=7 * 24 * 3600):
        # if exist
        if self.r.exists(index_key):
            # copy old first
            self.r.copy(index_key, index_key + '_old', replace=True)
        # use pipeline to package requests (this is not an atom transaction)
        pipe = self.r.pipeline(transaction=True)
        pipe.delete(index_key)
        pipe.zadd(name=index_key, mapping=item_list)
        pipe.expire(index_key, ttl)
        pipe.expire(index_key + '_old', ttl)
        pipe.execute()

    def update_hash(self, key, item_dic, ttl=7 * 24 * 3600):
        for it in item_dic:
            if isinstance(item_dic[it], list):
                item_dic[it] = str(item_dic[it])
                # print('转换为列表：{} '.format(item_dic[it]))
        self.r.hset(name=key, mapping=item_dic)
        if ttl:
            self.r.expire(key, ttl)

    # 先检查，查到再更新
    def check_and_update_hash(self, key, item_dic, ttl=7 * 24 * 3600):
        if self.r.exists(key):
            self.r.hset(name=key, mapping=item_dic)
            if ttl:
                self.r.expire(key, ttl)
        else:
            print('未查询到key,跳过插入:', key)

    # 查询zset
    def zrange(self, index_key, start, end, desc=True, withscores=True):
        return self.r.zrange(index_key, start, end, True, True)

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
