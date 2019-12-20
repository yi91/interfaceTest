# coding:utf-8

import unittest

import paramunittest
from common.commondef import configHttp
from common import commondef, configDB
from common.Log import MyLog

get_event_list_xls = commondef.get_xls("apiCase.xlsx", "sec_get_event_list")
localConfigHttp = configHttp.ConfigHttp()
localConfigDB = configDB.MyDB()


@paramunittest.parametrized(*get_event_list_xls)
class GetEventListTest(unittest.TestCase):
    """ 查询发布会信息（带用户认证） """

    def setParameters(self, case_name, method, auth, id, name, result, code, msg):
        """ 初始化所有excel读取到的参数，不能放在setUp处理 """
        self.case_name = str(case_name)
        self.method = str(method)
        # 将认证信息转成元组
        self.auth_user = tuple(eval(auth))
        self.eid = str(id)
        self.name = str(name)
        self.result = str(result)
        self.status = str(code)
        self.message = str(msg)
        # 先声明两个变量留作后面用
        self.resp = None
        self.info = None

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()

    def test_get_event_list(self):
        """ auth为空 """
        # 1、set url
        self.url = commondef.get_url_from_xml('sec_get_event_list')
        # 获取完整的url，必须重新赋值self.url
        self.url = localConfigHttp.set_url(self.url)

        # 2、set header

        # 3、set params
        localConfigHttp.set_params({"eid": self.eid, 'name': self.name})
        # 4、test interface，手动添加一个auth参数
        self.resp = localConfigHttp.get(self.auth_user)

        # 5、check result
        self.checkResult()

    def checkResult(self):
        """ 查询数据库，检查结果是否正确 """
        # 1、格式化接口返回的信息
        self.info = self.resp.json()
        # 2、向html展示返回的信息
        commondef.show_return_msg(self.resp)

        # 根据result的结果，判断是否需要再检查一遍数据库
        if self.result == '0':  # 不用检查
            self.assertEqual(str(self.info['status']), self.status)
            self.assertIn(self.message, self.info['message'])

        # 需要检查数据库
        if self.result == '1':
            self.assertEqual(self.info['status'], self.status)
            self.assertIn(self.message, self.info['message'])

            # get_sql的参数全靠手写
            sql = commondef.get_sql('guest', 'sign_guest', 'get_event_list')
            if self.eid != '':
                localConfigDB.executeSQL(sql, self.eid)
            elif self.name != '':
                localConfigDB.executeSQL(sql, self.name)
            localConfigDB.closeDB()

    def tearDown(self):
        # 输出到html查看
        print(self.result)
        # 输出到日志文件查看
        self.log.build_case_line(self.case_name, str(self.info['status']), self.info['message'])


if __name__ == '__main__':
    unittest.main()
