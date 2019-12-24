# coding:utf-8

import unittest
import paramunittest
from common import Log
import readConfig
from common import commondef
from common import configHttp as ConfigHttp

login_xls = commondef.get_xls("userCase.xlsx", "bloglogin")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*login_xls)
class Login(unittest.TestCase):
    # 注意字段的名称要和表格内的字段名称一一对应
    def setParameters(self, case_name, method, token, data1, data2, result, code, msg):
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param data1:
        :param data2:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.data1 = str(data1)
        self.data2 = str(data2)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.return_json = None
        self.info = None

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name + "测试开始前准备")

    def testLogin(self):
        """
        test body
        :return:
        """
        # set url
        self.url = commondef.get_url_from_xml('bloglogin')
        self.url = configHttp.set_url(self.url)
        print("第一步：设置url  " + self.url)

        # get visitor token
        if self.token == '0':
            token = localReadConfig.get_headers("token_v")

            # set headers
            header = {"token": str(token)}
            configHttp.set_headers(header)
            print("第二步：设置header(token等)" + self.headers)

        elif self.token == '1':
            pass

        # set params
        data = {}
        configHttp.set_data(data)
        print("第三步：设置发送请求的参数" + self.data)

        # test interface
        if self.method == 'get':
            self.return_json = configHttp.get()
            # method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        else:
            self.return_json = configHttp.post()

        print("第四步：发送请求\n\t\t请求方法：" + self.method)

        # check result
        # self.checkResult()
        print("第五步：检查结果")

    def tearDown(self):
        """

        :return:
        """
        # info = self.info
        if self.code == 0:
            # get uer token
            token_u = commondef.get_value_from_return_json(info, 'member', 'token')
            # set user token to config file
            localReadConfig.set_headers("TOKEN_U", token_u)
        else:
            pass
        # self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])
        self.log.build_case_line(self.case_name, self.code, self.msg)
        print("测试结束，输出log完结\n")

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        # show return message
        commondef.show_return_msg(self.return_json)

        if self.result == '0':
            data1 = commondef.get_value_from_return_json(self.info, 'member', 'data1')
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            self.assertEqual(data1, self.data1)

        if self.result == '1':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)


if __name__ == '__main__':
    unittest.main()
