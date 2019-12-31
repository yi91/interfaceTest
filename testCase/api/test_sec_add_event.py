# coding:utf-8
import hashlib
import time
import unittest
import paramunittest

from common import commondef, configHttp, configDB
from common.Log import MyLog

add_event_xml = commondef.get_xls('apiCase.xlsx', 'sec_add_event')
localConfigHttp = configHttp.ConfigHttp()
localConfigDB = configDB.MyDB()


@paramunittest.parametrized(*add_event_xml)
class SecAddEvntTest(unittest.TestCase):
    """ 测试添加发布会（带签名） """

    def setParameters(self, case_name, method, data, result, code, msg):
        self.case_name = case_name
        self.method = method
        self.ori_data = data
        self.result = int(result)
        self.code = code
        self.msg = msg

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name + '\n\n')

        # 创建客户端的数字签名
        now_time = time.time()
        self.client_time = str(now_time).split('.')[0]

        md5 = hashlib.md5()
        self.api_key = self.client_time + "&Guest-Bugmaster"
        sign_bytes_utf8 = self.api_key.encode(encoding="utf-8")
        # 开始加密
        md5.update(sign_bytes_utf8)
        self.client_sign = md5.hexdigest()

        # eval可以自动把self.client_time解析成变量，并且把excel的数字变成int
        self.data = eval(self.ori_data)

    def test_sec_add_event(self):
        # 1、set url
        url = commondef.get_url_from_xml('sec_add_event')
        # 获取完整的self.url
        self.url = localConfigHttp.set_url(url)
        print("1、请求的地址：" + self.url)

        # 2、set headers

        # 3、set params
        localConfigHttp.set_data(self.data)
        print("3、发送请求的参数：" + self.ori_data)

        # 4、test interface
        self.resp = localConfigHttp.post()
        self.info = self.resp.json()
        print('4、发送请求的方法：' + self.method)
        self.assertEqual(str(self.info['status']), self.code)
        self.assertIn(self.msg, self.info['message'])

        # 5、check result
        self.checkResult()

    def checkResult(self):
        """ 查询数据库，检查结果是否正确 """

        # 1、向html展示返回的信息
        commondef.show_return_msg(self.resp)

        # 根据result的值，检查数据库
        if self.result == 1:
            # get_sql的参数全靠手写
            sql = commondef.get_sql('guest', 'sign_event', 'sec_get_event_list')
            # self.eid if self.eid != '' else ''，三元运算符，前面为真后面为假
            id = self.data['eid'] if self.data['eid'] != '' else ''
            name = self.data['name'] if self.data['name'] != '' else ''
            cursor = localConfigDB.executeSQL(sql, (id, name))

            if cursor is not None:
                self.logger.info("查询数据库成功")
                print("查询数据库成功")

            # 关闭数据库连接前，先删除旧数据
            del_sql = commondef.get_sql('guest', 'sign_event', 'delete_event')
            del_cursor = localConfigDB.executeSQL(del_sql, (id, name))
            if del_cursor is not None:
                self.logger.info("删除旧数据成功")
                print("删除旧数据成功")

            # 关闭连接
            localConfigDB.closeDB()

    def tearDown(self):
        # 输出到日志文件
        self.log.build_case_line(self.case_name, self.info['status'], self.info['message'])
        print("测试结束，输出log完结\n\n")


if __name__ == '__main__':
    unittest.main()
