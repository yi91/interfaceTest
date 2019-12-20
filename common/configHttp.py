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
    def get(self, auth_user):
        """
        defined get method
        :return:
        """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params,
                                    timeout=float(timeout), auth=auth_user)
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
            response = requests.post(self.url, headers=self.headers, params=self.params,
                                     data=self.data, timeout=float(timeout))
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


if __name__ == "__main__":
    params = "?ie=utf-8&newi=1&mod=1&isid=d96a47a400106206&" \
             "wd=pycharm%E5%A4%9A%E8%A1%8C%E6%B3%A8%E9%87%8A%E7%9A%84%E5%BF%AB%E6%8D%B7%E9%94%AE&" \
             "rsv_spt=1&" \
             "rsv_iqid=0xc27cf0ff0016501c&" \
             "issp=1&f=3&" \
             "rsv_bp=1&" \
             "rsv_idx=2&" \
             "rqlang=cn&tn=baiduhome_pg&" \
             "rsv_dl=ts_0&" \
             "rsv_enter=0&" \
             "rsv_t=07459LZKDDWf8SBkXEk1YKpQRiq8jPT5U5IBJs1R9FNlq3rn%2F781hyPtzSQ7cY2fA326&" \
             "rsv_sug3=32&" \
             "oq=pycharm%25E5%25A4%259A%25E8%25A1%258C%25E6%25B3%25A8%25E9%2587%258A%25E7%259A%2584%25E5%25BF%25AB%25E6%258D%25B7%25E9%2594%25AE&" \
             "rsv_pq=d96a47a400106206&prefixsug=pycharm%25E5%25A4%259A%25E8%25A1%258C%25E6%25B3%25A8%25E9%2587%258A%25E7%259A%2584%25E5%25BF%25AB%25E6%258D%25B7%25E9%2594%25AE&" \
             "rsp=0&" \
             "rsv_sug4=8374&" \
             "bs=pycharm%E5%A4%9A%E8%A1%8C%E6%B3%A8%E9%87%8A%E7%9A%84%E5%BF%AB%E6%8D%B7%E9%94%AE&" \
             "rsv_sid=1456_21091_30211_30124&" \
             "_ss=1&clist=&hsug=&f4s=1&csor=15&_cr1=55260"
    ch = ConfigHttp()
    ch.set_url("/s")
    ch.set_params(params)

    print(ch.get().status_code)
