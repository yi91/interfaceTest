# coding:utf-8

import logging
import threading
from common.read_config import ReadConfig


class Log:
    def __init__(self, logger_name):

        # 获取logging的实例
        self.logger = logging.getLogger(logger_name)
        # 设置日志级别
        self.logger.setLevel(logging.INFO)

        # 日志路径
        self.rp = ReadConfig().get_report()
        self.log_path = self.rp + 'output.log'

        # FileHandler用于输出log到文件
        fh = logging.FileHandler(self.log_path, encoding='utf-8')
        # 再创建一个StreamHandler，用于输出log到控制台，可以单独控制log级别
        sh = logging.StreamHandler()

        # 设置log格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)

    def get_logger(self):
        return self.logger

    def build_start_line(self, case_no):
        """ 添加用例开始线条"""
        self.logger.info("--------" + case_no + " START--------")

    def build_end_line(self, case_no):
        """ 添加用例结束线条"""
        self.logger.info("--------" + case_no + " END--------")

    def build_case_line(self, case_name, code, msg):
        """ 记录用例报错信息 """
        self.logger.info(case_name+" - Code:"+str(code)+" - msg:"+msg)

    def write_result_to_log(self, result):
        """ 把用例测试结果写入 log 文件 """
        try:
            with open(self.log_path, "a+") as fp:
                fp.write(result)
            self.logger.info('测试结果写入 log 文件成功')
        except Exception as ex:
            self.logger.error(ex)


# 单独启用一个线程记录log日志，测试有效
class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    # 定义静态方法，方便调用
    @staticmethod
    def logger(log_name):
        if MyLog.log is None:
            MyLog.mutex.acquire()
            # 关联MyLog和Log的实例，当 MyLog.log 记录完操作再运行主测试程序
            MyLog.log = Log(log_name).get_logger()
            # 释放子线程，运行主程序
            MyLog.mutex.release()
        return MyLog.log


if __name__ == "__main__":
    logger = MyLog.logger()
    # 日志级别：DEBUG < INFO < WARN < ERROR，高于logger.setLevel的才会记录
    logger.debug("test debug")
    logger.info("test info")

