import unittest
import paramunittest
from common.logger import MyLog
from common import common_def, read_config as readConfig
from common import config_http

localGenerate_xls = commondef.get_xlsx("userCase.xlsx")
localConfigHttp = configHttp.ConfigHttp()
localReadConfig = readConfig.ReadConfig()


@paramunittest.parametrized(*localGenerate_xls)
class Generate(unittest.TestCase):

    def setParameters(self, case_name, method, result, code, msg):
        """
        set parameters
        :param case_name:
        :param method:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
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

    def testGenerate(self):
        """
        test body
        :return:
        """
        # set url
        self.url = commondef.get_url_from_xml('generate')
        localConfigHttp.set_url(self.url)

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
        check test reslt
        :return:
        """
        self.info = self.response.json()
        commondef.show_return_msg(self.response)

        if self.result == '0':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
