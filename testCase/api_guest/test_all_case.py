import json
import unittest
from ddt import ddt, data, unpack
from common import common_def as cd
from common.config_http import ConfigHttp
from common.config_db import MyDB

ch = ConfigHttp()
db = MyDB()
app, wb, sheet = cd.open_excel('case_guest.xlsx')
case_list = cd.get_xlsx(sheet)

@ddt
class TestAllCase(unittest.TestCase):
    """ 测试 api_django_rest 的 users 接口 """

    @classmethod
    def tearDownClass(cls):
        # 所有用例执行完就关闭excel
        cd.close_excel(app, wb)
        # 所有用例执行完，关闭数据库连接
        db.close_db()

    @data(*case_list)
    @unpack
    def test_all_case(self, case_name, method, header, url, datas, is_run, result, response, msg, insert_sql, del_sql):
        self.case_name = case_name
        self.method = ch.set_method(method)
        self.header = ch.set_headers(header)
        self.url = ch.set_url(url)
        self.params = ch.set_data(datas)
        self.is_run = is_run
        self.result = result
        self.resp = response
        self.msg = msg
        self.insert_sql = insert_sql
        self.del_sql = del_sql

        # 先执行数据初始化操作
        if self.insert_sql is not None:
            for sql in self.insert_sql.strip().split(';'):
                # split分割的最后一个元素是None
                if sql != '' and not sql.isspace():
                    db.execute_sql(sql + ';')
        # 开始执行测试
        self.r = None
        if self.method == 'get':
            self.r = ch.get(self.case_name)
        elif self.method == 'post':
            if self.header is None or ('multipart/form-data' in self.header):
                self.r = ch.post(self.case_name)
            elif 'application/json' in self.header:
                ch.data = json.dumps(self.params)
                self.r = ch.post(self.case_name)
            else:
                # 发文件的待完善
                self.r = ch.post_with_file(self.case_name)
        elif self.method == 'dubbo':
            self.r = ch.dubbo(self.case_name)
        else:
            # 如果method不属于以上任何一种，就调用下面的方法
            self.r = ch.send_request(self.case_name)

        # 测试结束，必须在断言之前将结果写入excel，因为断言失败不会再继续执行后面的代码；或者放在teardown里面也行
        cd.write_resp_to_excel(sheet, self.case_name, self.r, self.msg)

        # 将数据库测试数据还原
        if self.del_sql is not None:
            for sql in self.del_sql.strip().split(';'):
                # split分割的最后一个元素是None
                if sql != '' and not sql.isspace():
                    db.execute_sql(sql + ';')

        # 请求结束，开始断言
        if self.r is None:
            self.assertEqual(1, 2)
        else:
            self.assertIn(self.msg, self.r.text)
            self.assertEqual(self.r.status_code, 200)










