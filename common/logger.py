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


if __name__ == "__main__":
    logger = Log.get_logger()
    # 日志级别：DEBUG < INFO < WARN < ERROR，高于logger.setLevel的才会记录
    logger.debug("test debug")
    logger.info("test info")

