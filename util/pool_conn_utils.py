import time
import pymysql
import pymysql.cursors
import threading
import psycopg2
import psycopg2.extras

# from DBUtils.PooledDB import PooledDB, SharedDBConnection #DBUtils 1.3
from dbutils.pooled_db import PooledDB, SharedDBConnection  # DButils 2.0


class pool_util():

    def __init__(self, host_user_password_prot_list, db_type='mysql'):
        self.db_type = db_type
        if db_type == 'postgresql':
            self.host_user_password_prot_list = host_user_password_prot_list
            self.POOL = PooledDB(
                creator=psycopg2,  # 使用链接数据库的模块
                maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
                mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
                maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
                maxshared=3,
                # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
                blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
                setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
                ping=0,
                # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
                host=self.host_user_password_prot_list[0],
                port=self.host_user_password_prot_list[4],
                user=self.host_user_password_prot_list[1],
                password=self.host_user_password_prot_list[2],
                database=self.host_user_password_prot_list[3],
                # charset='utf8'
            )
        else:
            self.host_user_password_prot_list = host_user_password_prot_list
            self.POOL = PooledDB(
                creator=pymysql,  # 使用链接数据库的模块
                maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
                mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
                maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
                maxshared=3,
                # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
                blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
                setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
                ping=0,
                # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
                host=self.host_user_password_prot_list[0],
                port=self.host_user_password_prot_list[4],
                user=self.host_user_password_prot_list[1],
                password=self.host_user_password_prot_list[2],
                database=self.host_user_password_prot_list[3],
                charset='utf8'
            )

    # 打开连接
    def create_conn(self):
        conn = self.POOL.connection()
        if self.db_type == 'postgresql':
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        return conn, cursor

    # 打开连接2,非dic的cursor
    def create_conn2(self):
        conn = self.POOL.connection()
        cursor = conn.cursor()
        return conn, cursor

    # 关闭连接
    def close_conn(self, conn, cursor):
        cursor.close()
        conn.close()

    # 插入一条数据
    def insert(self, sql, args=None):
        conn, cursor = self.create_conn()
        res = cursor.execute(sql, args)
        conn.commit()
        self.close_conn(conn, cursor)
        return res

    # 查询一条数据
    def fetch_one(self, sql):
        conn, cursor = self.create_conn()
        cursor.execute(sql)
        res = cursor.fetchone()
        self.close_conn(conn, cursor)
        return res

    # # 查询一条数据
    # def fetch_one(self,sql):
    #     conn,cursor = self.create_conn2()
    #     cursor.execute(sql)
    #     res = cursor.fetchone()
    #     self.close_conn(conn,cursor)
    #     return res

    # 查询所有数据
    def fetch_all(self, sql, args=None):
        conn, cursor = self.create_conn()
        cursor.execute(sql, args)
        res = cursor.fetchall()
        self.close_conn(conn, cursor)
        return res

    # 手动多次执行sql列表
    def execute(self, args):
        conn, cur = self.create_conn()
        re = 0
        cur.execute(args)
        re += cur.rowcount
        conn.commit()
        self.close_conn(conn, cur)
        return re

    # 手动多次执行sql列表
    def executemany2_sql(self, args):
        conn, cur = self.create_conn()
        re = 0
        for a in args:
            cur.execute(a)
            re += cur.rowcount
        conn.commit()
        self.close_conn(conn, cur)
        return re

    # 插入助手
    def insert_one_helper(self, table_name, column_list: list, value_list: list):
        sql = "insert into " + table_name + ' ('
        sql += ','.join(column_list)
        sql += ') values ( '
        value_list = [str(x) for x in value_list]
        for value in value_list:
            value = value.replace("'", "''")  # 一个引号变为两个引号即可
            sql += "'"
            sql += value
            sql += "',"
        sql = sql[:-1]
        sql += ')'
        self.execute(sql)
