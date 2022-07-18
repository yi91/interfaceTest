# coding:utf-8
from common.read_config import ReadConfig
from common.logger import Log
import common.common_def as cd
import json
import requests

rc = ReadConfig()
logger = Log('ConfigHttp').get_logger()


class ConfigHttp:

    host = rc.get_http("base_url")
    timeout = rc.get_http("timeout")

    def __init__(self):
        self.url = None
        self.method = None
        self.headers = None
        self.data = None
        self.file = None

    def set_url(self, url):
        self.url = self.host + url
        logger.info('请求的url：%s' % self.url)
        return self.url

    def set_method(self, method):
        self.method = method
        logger.info('请求方式：%s' % self.method)
        return self.method

    # 不同于readConfig的set_header
    def set_headers(self, header):
        if header is not None:
            # 第一步格式化excel中的headers，返回dic类型的数据
            try:
                self.headers = json.loads(header)
            except Exception:
                self.headers = eval(header)
            # 判断接口是否需要token
            if 'token' in header:
                token = cd.get_token()
                # 将token添加到dic类型的self.headers
                self.headers["token"] = token
            logger.info('请求头：%s' % self.headers)
        return self.headers

    # 将从文件得到的string类型data转成json对象
    def set_data(self, data):
        if data is not None:
            try:
                self.data = json.loads(data)
            except Exception:
                self.data = eval(data)
            logger.info('请求的json参数：%s' % self.data)
        return self.data

    def get(self, case_name):
        """ 封装get请求 """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.data,
                                    timeout=float(self.timeout))
            logger.info('用例 %s 请求成功。' % case_name)
            return response
        except Exception as e:
            logger.error('用例 %s 请求错误，请检查参数' % case_name, e)
            return e

    def post(self, case_name):
        """ 封装 post请求 """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, timeout=float(self.timeout))
            logger.info('用例 %s 请求成功。' % case_name)
            return response
        except Exception as e:
            logger.error('用例 %s 请求错误' % case_name, e)
            return e

    def post_with_file(self, case_name):
        """ 封装上传文件的 post 请求 """
        if self.file != '':
            try:
                with open(self.file, 'rb') as fp:
                    response = requests.post(self.url, headers=self.headers, data=self.data, files=fp,
                                             timeout=float(self.timeout))
                logger.info('用例 %s 请求成功。' % case_name)
                return response
            except Exception as e:
                logger.error('用例 %s 请求错误' % case_name, e)
                return e
        else:
            self.post(case_name)

    def dubbo(self, case_name):
        """ 封装dubbo类型的接口
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
        """
        pass

    def send_request(self, method, url, headers=None, data=None, **kwargs):
        if headers is not None:
            headers = json.dumps(headers).lower()
        if isinstance(data, str):
            try:
                # 将字符串类型的 data 转成json对象，如果data里面有特殊符号，就使用 eval 转换
                data = json.loads(data)
            except Exception:
                # json.loads无法处理字符串元素有特殊符号，所以使用eval
                data = eval(data)
        if 'get' == method.lower():
            response = requests.get(url=url, headers=headers, params=data, **kwargs)
        elif 'post' == method.lower():
            if headers is None:
                response = requests.post(url=url, data=data, **kwargs)
            elif 'application/x-www-form-urlencode' in headers:
                headers = json.loads(headers)
                response = requests.post(url=url, headers=headers, data=data, **kwargs)
            elif 'application/json' in headers:
                headers = json.loads(headers)
                response = requests.post(url=url, headers=headers, json=data, **kwargs)
            else:
                # 如果headers不属于以上任何一种，就调用下面的方法
                headers = json.loads(headers)
                response = requests.request(method=method, url=url, headers=headers, **kwargs)
        else:
            raise ValueError('request method "{}" error ! please check.'.format(method))
        return response


if __name__ == "__main__":
    params = ""
    ch = ConfigHttp()
    ch.set_url("/s")
    ch.set_data(params)

    print(ch.get('caseName：请求参数1为空').status_code)
