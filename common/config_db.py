# coding:utf-8

import pymysql.cursors
from common.read_config import ReadConfig
from common.logger import Log

rc = ReadConfig()
logger = Log('MyDB').get_logger()


class MyDB:

    def __init__(self):
        try:
            # 创建数据库连接
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
            logger.error('数据库连接失败，请检查', e)

    # 获取sql执行完的self.cursor
    def execute_sql(self, sql):
        # 先执行 db.ping(reconnect=True)，可以保证连接丢失时自动重连
        self.db.ping(reconnect=True)
        try:
            # 使用 execute()方法执行SQL，insert返回结果是dic类型的cursor，delete的返回值是执行结果的条数
            self.cursor.execute(sql)
            # 手动提交执行
            self.db.commit()
            # 打印sql时，必须用format，否则logging报错
            logger.info('sql执行成功 {}'.format(sql))
        except Exception as e:
            logger.error('sql执行失败，请检查 \n %r' % e)
        finally:
            # 返回游标对象
            return self.cursor

    @staticmethod
    def get_all(cursor):
        """ 以list形式返回select语句执行完的结果，每行结果以dic形式当作list的元素 """
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
