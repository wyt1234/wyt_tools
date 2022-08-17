from util import pool_conn_utils
from loguru import logger


class postgres_helper_class:
    def __init__(self, host, user, password, database, port):
        self.pool = pool_conn_utils.pool_util([host, user, password, database, port], db_type='postgresql')
        logger.info('接入postgres：{}:{}/{}', host, port, database)

    # 去掉句子里的换行符和空格
    def strip_sentence(input_sentence: str):
        return input_sentence.replace('\n', ' ').replace(' ', '').replace('\u3000', '')

    # 检查 - 更新 - 查询同步
    def check_update_query(self, item, **kwargs):
        mongo_id = item.get('mongo_id') or item.get('_id')
        lv1 = kwargs.get('lv1') or '其他'
        source = item.get('source') or ''
        extract = item.get('keywords') or ''  # 公众号的keyword字段应该是抽取的关键词
        if isinstance(extract, list):
            extract = '、'.join(extract)
        url = item.get('url') or ''
        images = item.get('image') or item.get('images') or ''
        if isinstance(images, list):
            images = '、'.join(images)
        title = item['title']
        content = item['content'][:4000]
        keyword = item['hit_kw']
        # 计算w1 -> 暂为关键词数 +100 todo 质量分算法
        if keyword:
            w1 = len(keyword.split('、')) + 100
        else:
            w1 = 100
        content_cut = content[:200]
        html = item.get('html')  # 原文完整html -> 先不存暂时没用
        sql = "select w1,view,click,love,collect,dislike from recsys_item where mongo_id = '%s'" % mongo_id
        db_item = self.pool.fetch_one(sql)
        # 不存在则插入 -> 插入完重新查询
        if not db_item:
            table_name = 'recsys_item'
            column_list = ['title', 'mongo_id', 'content', 'keyword', 'extract', 'content_cut', 'html', 'lv1', 'source',
                           'url', 'images', 'w1']
            value_list = [title, mongo_id, content, keyword, extract, content_cut, '', lv1, source, url, images, w1]
            try:
                self.pool.insert_one_helper(table_name, column_list, value_list)
            except Exception as e:
                logger.warning("插入postgres时发生错误：{}", e)
                return
            # 插入完重新查询
            db_item = self.pool.fetch_one(sql)
            # logger.info('插入postgres：{},{}', mongo_id, title)
        # 已存在则直接同步到输入
        item['w1'] = db_item['w1']
        item['view'] = db_item['view']
        item['click'] = db_item['click']
        item['love'] = db_item['love']
        item['collect'] = db_item['collect']
        item['dislike'] = db_item['dislike']
        return
