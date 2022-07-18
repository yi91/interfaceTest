import unittest
import paramunittest
from common import common_def as cc
from common.config_http import ConfigHttp


ch = ConfigHttp()
case_list = cc.get_xlsx('case_template.xlsx')


@paramunittest.parametrized(*case_list)
class TestUsers(unittest.TestCase):
    """ 测试 django_test 的 users 接口 """
    def setParameters(self, case_name, method, header, url, data, is_run, result, response, msg, insert_sql, del_sql):
        """ 方法名必须是setParameters """
        self.case_name = case_name
        self.method = ch.set_method(method)
        self.header = ch.set_headers(header)
        self.url = ch.set_url(url)
        self.params = ch.set_data(data)
        self.is_run = is_run
        self.result = result
        self.resp = response
        self.msg = msg
        self.insert_sql = insert_sql
        self.del_sql = del_sql

    def test_user(self):
        self.r = ch.get(self.case_name)
        if self.r is None:
            self.assertEqual(1, 2)
        else:
            self.assertIn(self.msg, self.r.text)
            self.assertEqual(self.r.status_code, 200)
        cc.write_resp_to_excel('case_template.xlsx', self.case_name, self.r, self.msg)








