# coding:utf-8
import os
import configparser

# 注意，如果单独运行某个用例，则此处的proDir 路径会出错，建议使用runAll.py 执行用例
configPath = os.path.dirname(os.path.dirname(__file__)) + "\\testFile\\config.ini"


class ReadConfig:
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def get_report(self):
        # 返回值默认str类型
        value = self.cf.get('REPORT', 'report_path')
        return value

    def set_report(self, value):
        self.cf.set("REPORT", 'report_path', value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_header(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    # 写入内容到 header，cf对象先读取所有内容再set，最后write的时候相当于先清空文件所有内容再把cf事先读取的写入
    def set_header(self, name, value):
        self.cf.set("HEADERS", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value


# 测试ReadConfig的功能
if __name__ == '__main__':
    rc = ReadConfig()
    print(rc.get_db(name="username"))
