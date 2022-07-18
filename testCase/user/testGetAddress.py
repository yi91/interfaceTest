import unittest
import paramunittest
from common import logger as Log, read_config as readConfig
from common import common_def
from common import config_http as ConfigHttp
from common import businessCommon

getAddress_xls = commondef.get_xlsx("userCase.xlsx")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*getAddress_xls)
class GetAddress(unittest.TestCase):
    def setParameters(self, case_name, method, token, address_id, result, code, msg):
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param address_id:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.address_id = str(address_id)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
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
        self.log = Log.MyLog.logger()
        self.logger = self.log.logger()
        self.login_token = businessCommon.login()

    def testGetAddressList(self):
        """
        test body
        :return:
        """
        # set url
        self.url = commondef.get_url_from_xml('getAddress')
        configHttp.set_url(self.url)

        # get token
        if self.token == '0':
            token = self.login_token
        else:
            token = self.token

        # set headers
        header = {"token": str(token)}
        configHttp.set_headers(header)

        # set params
        params = {"address_id": self.address_id}
        configHttp.set_params(params)

        # test interface
        self.return_json = configHttp.get()

        # check report
        self.checkResult()

    def tearDown(self):
        """

        :return:
        """
        businessCommon.logout(self.login_token)
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])

    def checkResult(self):
        """

        :return:
        """
        self.info = self.return_json.json()
        commondef.show_return_msg(self.return_json)

        if self.result == '0':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            self.assertIsNotNone(self.info['info']['address'])
            value = commondef.get_value_from_return_json(self.info, "address", "addressId")
            self.assertEqual(value, self.address_id)

        if self.result == '1':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
