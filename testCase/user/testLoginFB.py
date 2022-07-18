import unittest
import paramunittest
from common.logger import MyLog
from common import common_def, read_config as readConfig
from common import config_http

localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localLoginFB_xls = commondef.get_xlsx("userCase.xlsx")


@paramunittest.parametrized(*localLoginFB_xls)
class LoginFB(unittest.TestCase):

    def setParameters(self, case_name, method, token, email, facebook_id, fbtoken, invite_agency, code, msg):
        """
        set parameters
        :param case_name:
        :param method:
        :param token:
        :param email:
        :param facebook_id:
        :param fbtoken:
        :param invite_agency:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.email = str(email)
        self.facebook_id = str(facebook_id)
        self.fbtoken = str(fbtoken)
        self.invite_agency = str(invite_agency)
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

    def testLoginFB(self):
        """
        test body
        :return:
        """
        # set url
        self.url = commondef.get_url_from_xml('loginFb')
        localConfigHttp.set_url(self.url)

        # set header
        if self.token == '0':
            token = localReadConfig.get_header("token_v")
        elif self.token == '1':
            token = None
        header = {'token': token}
        localConfigHttp.set_headers(header)

        # set params
        if self.invite_agency == '':
            self.invite_agency = int(0)
        data = {'email': self.email,
                'facebook_id': self.facebook_id,
                'fbtoken': self.fbtoken,
                'invite_agency': self.invite_agency
                }
        localConfigHttp.set_data(data)

        # test interface
        if self.method == 'get':
            self.response = localConfigHttp.get()
        elif self.method == 'post':
            self.response = localConfigHttp.post()
        else:
            self.logger.info("No this interface's method:" + self.method)

        # check report
        self.checkResult()

    def tearDown(self):
        """

        :return:
        """
        pass

    def checkResult(self):
        """
        check test report
        :return:
        """
        self.info = self.response.json()
        commondef.show_return_msg(self.response)
        self.assertEqual(self.info['code'], self.code)
        if self.info['code'] == self.code:
            self.assertEqual(self.info['msg'], self.msg)
            self.log.build_OK_line(self.case_name, self.code, self.msg)
        else:
            self.log.build_NG_line(self.case_name, self.info['code'], self.info['msg'])
