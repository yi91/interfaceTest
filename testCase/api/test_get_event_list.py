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

    def setParameters(self, case_name, method, id, name, auth, result, code, msg):
        """
        初始化所有excel读取到的参数，不能放在setUp处理
        加str()确保格式正确
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.eid = str(id)
        self.name = str(name)
        self.auth = str(auth)
        self.result = str(result)
        self.status = str(code)
        self.message = str(msg)

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name+'\n\n')

    def test_get_event_list(self):

        # 1、set url
        url = commondef.get_url_from_xml('sec_get_event_list')
        # 获取完整的self.url
        self.url = localConfigHttp.set_url(url)
        print("1、请求的地址：" + self.url)

        # 2、set headers
        self.header = {'authorization': 'Basic '+commondef.my_base64(self.auth)}
        localConfigHttp.set_headers(self.header)
        print("2、设置header：" + str(self.header))

        # 3、set params
        localConfigHttp.set_params({"eid": self.eid, 'name': self.name})
        print("3、发送请求的参数：" + str({"eid": self.eid, 'name': self.name}))

        # 4、test interface
        self.resp = localConfigHttp.get()
        print('4、发送请求的方法：' + self.method)

        # 5、check result
        self.checkResult()
        print("5、检查结果")

    def checkResult(self):
        """ 查询数据库，检查结果是否正确 """
        # 1、向html展示返回的信息
        commondef.show_return_msg(self.resp)

        self.info = self.resp.json()
        # 根据result的结果，判断是否需要再检查一遍数据库
        if self.result == '0':  # 不用检查
            self.assertEqual(str(self.info['status']), self.status)
            self.assertIn(self.message, self.info['message'])

        # 需要检查数据库
        if self.result == '1':
            self.assertEqual(str(self.info['status']), self.status)
            self.assertIn(self.message, self.info['message'])

            # get_sql的参数全靠手写
            sql = commondef.get_sql('guest', 'sign_event', 'sec_get_event_list')
            # self.eid if self.eid != '' else ''，三元运算符，前面为真后面为假
            id = self.eid if self.eid != '' else ''
            name = self.name if self.name != '' else ''
            cursor = localConfigDB.executeSQL(sql, (id, name))

            if cursor is not None:
                print("查询数据库成功")
            localConfigDB.closeDB()

    def tearDown(self):
        # 输出到日志文件
        self.log.build_case_line(self.case_name, self.info['status'], self.info['message'])
        print("测试结束，输出log完结\n\n")


if __name__ == '__main__':
    unittest.main()
