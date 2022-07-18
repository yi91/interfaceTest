# coding:utf-8

import pymysql.cursors
from common import read_config as readConfig
from common.logger import MyLog

rc = readConfig.ReadConfig()
logger = MyLog.logger('MyDB')


class MyDB:

    def __init__(self):
        try:
            # 打开数据库连接
            self.db = pymysql.connect(host=rc.get_db("host"),
                                      user=rc.get_db("username"),
                                      password=rc.get_db("password"),
                                      port=int(rc.get_db("port")),
                                      db=rc.get_db("database"),
                                      charset='utf8',
                                      cursorclass=pymysql.cursors.DictCursor)
            # 使用 cursor() 方法创建一个游标对象 cursor
            self.cursor = self.db.cursor()
            logger.info("Connect DB successfully!")
        except Exception as e:
            logger.error('数据库连接失败，请检查 \n %r' % e)

    def execute_sql(self, sql, params):
        # 先执行 db.ping(reconnect=True)，可以保证连接丢失时自动重连
        self.db.ping(reconnect=True)
        try:
            # 使用 execute()方法执行SQL查询，多个参数传入时需要用集合形式如 list或者tuple 等，查询和删除的返回值是结果的条数
            self.cursor.execute(sql, params)
            # 手动提交执行
            self.db.commit()
            logger.info('sql执行成功：%s' % sql)
        except Exception as e:
            logger.error('sql执行失败，请检查 \n %r' % e)
        finally:
            # 返回游标对象
            return self.cursor

    @staticmethod
    def get_all(cursor):
        """ 查询数据库所有记录 """
        value = cursor.fetchall()
        return value

    @staticmethod
    def get_one(cursor):
        """ 使用 fetchone() 方法获取单条数据 """
        value = cursor.fetchone()
        return value

    def close_db(self):
        self.db.close()
        logger.info("Database connection closed.")


if __name__ == '__main__':
    mydb = MyDB()
