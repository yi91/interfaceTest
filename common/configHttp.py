# coding:utf-8

import requests
import readConfig
from common.Log import MyLog as Log
import json

localReadConfig = readConfig.ReadConfig()


class ConfigHttp:

    def __init__(self):
        global scheme, host, port, timeout

        scheme = localReadConfig.get_http("scheme")
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")

        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.state = 0

    def set_url(self, url):
        """
        set url
        :param: interface url的前面需要带上斜杠“\”
        :return:
        """
        self.url = scheme + '://' + host + ':' + port + url
        return self.url

    def set_method(self, method):
        """ 设置dubbo接口的测试方法 """
        self.method = method

    # 不同于readConfig的设置headers
    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header

    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.data = data

    def set_files(self, filename):
        """
        set upload files
        :param filename:
        :return:
        """
        if filename != '':
            file_path = 'F:/AppTest/Test/interfaceTest/testFile/img/' + filename
            self.files = {'file': open(file_path, 'rb')}

        if filename == '' or filename is None:
            self.state = 1

    # defined http get method
    def get(self):
        """
        defined get method
        :return:
        """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params,
                                    timeout=float(timeout))
            # 如果你的接口地址不正确,千万不能使用这个方法来抛出错误
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method，include get params and post data uninclude upload file
    def post(self):
        """
        defined post method，不包含上传文件
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data,
                                     timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method，include upload file
    def postWithFile(self):
        """
        defined post method，包含上传文件
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data,
                                     files=self.files, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # for json
    def postWithJson(self):
        """
        defined post method，针对入参是json的
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, json=json.dumps(self.data), timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    def dubbo(self):
        """ 测试dubbo类型的接口 """
        # 初始化dubbo对象
        conn = dubbo_telnet.connect(host, port)
        # 设置telnet连接超时时间
        conn.set_connect_timeout(10)
        # 设置dubbo服务返回响应的编码
        conn.set_encoding('gbk')

        # 显示服务列表
        # print(conn.do("ls"))
        # 显示指定服务的方法列表
        # print(conn.do("ls XXXService"))

        # 方法调用
        interface = 'XXXService'
        result = conn.invoke(interface, self.method, self.params)
        return json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '), skipkeys=True, ensure_ascii=False)


if __name__ == "__main__":
    params = ""
    ch = ConfigHttp()
    ch.set_url("/s")
    ch.set_params(params)

    print(ch.get().status_code)
