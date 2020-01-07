# coding:utf-8

import pymysql
import readConfig as readConfig
from common.Log import MyLog as Log

localReadConfig = readConfig.ReadConfig()


class MyDB:

    def __init__(self):
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        try:
            # 打开数据库连接
            self.db = pymysql.connect(host=localReadConfig.get_db("host"),
                                      user=localReadConfig.get_db("username"),
                                      password=localReadConfig.get_db("password"),
                                      port=int(localReadConfig.get_db("port")),
                                      db=localReadConfig.get_db("database"),
                                      charset='utf8',
                                      cursorclass=pymysql.cursors.DictCursor)
            # 使用 cursor() 方法创建一个游标对象 cursor
            self.cursor = self.db.cursor()
            print("Connect DB successfully!")
        except ConnectionError as ex:
            self.logger.error(str(ex))

    # def connectDB(self):
    #     """
    #     connect to database
    #     :return:
    #     """
    #     try:
    #         # 打开数据库连接
    #         self.db = pymysql.connect(**config)
    #         # 使用 cursor() 方法创建一个游标对象 cursor
    #         self.cursor = self.db.cursor()
    #         print("Connect DB successfully!")
    #     except ConnectionError as ex:
    #         self.logger.error(str(ex))

    def executeSQL(self, sql, params):
        """
        execute sql
        :param sql:
        :param params:
        :return:
        """
        # 先执行 db.ping(reconnect=True)，可以保证连接丢失时自动重连
        self.db.ping(reconnect=True)
        # 使用 execute()方法执行SQL查询，多个参数传入时需要用集合形式，list或者tuple等，查询和删除的返回值是行数
        self.cursor.execute(sql, params)
        # 手动提交执行
        self.db.commit()
        # 返回游标对象
        return self.cursor

    def get_all(self, cursor):
        """
        获取所有记录列表
        :param cursor:
        :return:
        """
        value = cursor.fetchall()
        return value

    def get_one(self, cursor):
        """
        使用 fetchone() 方法获取单条数据
        :param cursor:
        :return:
        """
        value = cursor.fetchone()
        return value

    def closeDB(self):
        """
        close database
        :return:
        """
        self.db.close()
        print("\nDatabase closed!")


if __name__ == '__main__':
    mydb = MyDB()
