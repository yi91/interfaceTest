import unittest
import paramunittest
from common import common_def as cc
from common.config_http import ConfigHttp
from ddt import ddt, data, unpack


ch = ConfigHttp()
case_list = cc.get_xlsx('case_django_rest.xlsx')


@ddt
class TestAllCase(unittest.TestCase):
    """ 测试 api_django_rest 的 users 接口 """

    @data(*case_list)
    @unpack
    def test_all_case(self, name, case_name, method, header, url, data, is_run, result,
                      response, msg, insert_sql, del_sql):
        ch.url = ch.set_url(url)
        ch.headers = ch.set_headers(header)
        ch.data = ch.set_data(data)
        self.r = None
        if method == 'get':
            self.r = ch.get(case_name)
        elif method == 'post':
            self.r = ch.post(case_name)
        elif method == 'dubbo':
            self.r = ch.dubbo(case_name)
        else:
            # 如果method不属于以上任何一种，就调用下面的方法
            self.r = ch.send_request(case_name)
        # 请求结束，开始断言并写入结果到excel
        if self.r is None:
            self.assertEqual(1, 2)
        else:
            self.assertIn(msg, self.r.text)
            self.assertEqual(self.r.status_code, 200)
        cc.write_resp_to_excel('case_django_rest.xlsx', case_name, self.r, msg)








