import unittest
import paramunittest
from common import common_def as cc
from common.config_http import ConfigHttp


ch = ConfigHttp()
case_list = cc.get_xlsx('case_guest.xlsx')


@paramunittest.parametrized(*case_list)
class TestAllCase(unittest.TestCase):
    """ 测试 api_django_rest 的 users 接口 """
    def setParameters(self, case_name, method, header, url, data, is_run, result,
                      response, msg, insert_sql, del_sql):
        """ 方法名必须是setParameters """
        # setParameters少写了excel表格前两列参数，因为get_xlsx方法已经过滤掉了前两列
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

    def test_all_case(self):
        self.r = None
        if self.method == 'get':
            self.r = ch.get(self.case_name)
        elif self.method == 'post':
            if self.header is None or ('multipart/form-data' in self.header):
                self.r = ch.post(self.case_name)
            elif 'application/json' in self.header:
                self.r = ch.post_json(self.case_name)
            else:
                # 待完善，还有问题
                self.r = ch.post_with_file(self.case_name)
        elif self.method == 'dubbo':
            self.r = ch.dubbo(self.case_name)
        else:
            # 如果method不属于以上任何一种，就调用下面的方法
            self.r = ch.send_request(self.case_name)
        # 请求结束，开始断言并写入结果到excel
        if self.r is None:
            self.assertEqual(1, 2)
        else:
            self.assertIn(self.msg, self.r.text)
            self.assertEqual(self.r.status_code, 200)
        cc.write_resp_to_excel('case_guest.xlsx', self.case_name, self.r, self.msg)








