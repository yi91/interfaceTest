import unittest
import paramunittest
from common.logger import MyLog
from common import common_def
from common import config_http
from common import businessCommon

localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localLogout_xls = commondef.get_xlsx("userCase.xlsx")


@paramunittest.parametrized(*localLogout_xls)
class Logout(unittest.TestCase):

    def setParameters(self, case_name, method, token, result, code, msg):
        """
        set parameters
        :param case_name:
        :param method:
        :param token:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.response = None
        self.info = None

    def description(self):
        """

        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = MyLog.logger()
        self.logger = self.log.logger()
        # login
        self.login_token = businessCommon.login()

    def testLogout(self):
        """
        test body
        :return:
        """
        # set url
        self.url = commondef.get_url_from_xml('logout')
        localConfigHttp.set_url(self.url)

        # set header
        if self.token == '0':
            token = self.login_token
        elif self.token == '1':
            token = localReadConfig.get_header("token_v")
        else:
            token = self.token
        header = {'token': token}
        localConfigHttp.set_headers(header)

        # test interface
        self.response = localConfigHttp.get()

        # check report
        self.checkResult()

    def tearDown(self):
        """

        :return:
        """
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])

    def checkResult(self):
        """
        check test report
        :return:
        """
        self.info = self.response.json()
        commondef.show_return_msg(self.response)

        if self.result == '0':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            self.assertEqual(self.info['info'], 1)
        if self.result == '1':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
