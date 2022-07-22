import json
import unittest

import paramunittest
# import requests
from requests.auth import HTTPBasicAuth
# from xlwings import App
# import common.common_def as cd
from common.read_config import ReadConfig
import datetime, time
# from common.config_db import MyDB
from ddt import ddt, data, unpack
from XTestRunner import HTMLTestRunner

# case = []
# path = r'/testFile/case_data/case_django_rest.xlsx'

'''
def xlwings_read():
    app = App(visible=False, add_book=False)
    try:
        wb = app.books.open(path)
        # time.sleep(5)
        # sheet = wb.sheets('Sheet1')
        sheet = wb.sheets['sheet1']
        # sheet = wb.sheets.active
        v = eval(sheet['D2'].value)
        print(type(v), v)
        # ran = sheet.used_range.shape
        # print(ran)
        # for r in range(ran[0] - 1):
        #     c = []
        #     for l in range(ran[1] - 1):
        #         if sheet[r + 1, l + 1] is None:
        #             c.append(None)
        #         else:
        #             c.append(sheet[r + 1, l + 1].value)
        #     case.append(c)
        #     print(c)
        # print(case)
        wb.close()
    except FileNotFoundError as e:
        print(e.args[0])
    finally:
        app.quit()


def send_request():
    url = 'http://127.0.0.1:8081/users/1/'

    # resp = requests.get(url, auth=HTTPBasicAuth('admin', 'admin123456'))
    # rc = ReadConfig()
    # rc.get_header()

    headers = {'Authorization': 'Basic YWRtaW46YWRtaW4xMjM0NTY='}
    # h = json.loads(headers)
    try:
        resp = requests.get(url, headers=headers)
        print(resp.status_code)
        print(json.dumps(resp.json(), ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':')))
        print(resp.json()['email'])
    except Exception as e:
        print('请求地址错误', e)

    # cd.write_resp_to_excel('case_django_rest.xlsx', 'test_users_auth_error', resp)
'''

def my_re():
    # jo = {
    #     "code": 200,
    #     "message": "登录成功",
    #     "token": "ef135bce4284s45ab5967fdf22e81fa2"
    # }
    jo = {"jjson": [
        {
            "code": 200,
            "message": "账号或密码错误",
            "token": " "
        },
        {"code": 200,
         "message": "登录成功",
         "token": "ef135bce4284s45ab5967fdf22e81fa2"
         }
    ]}
    # v = cd.get_value_from_response(json.dumps(jo, ensure_ascii=False), 'token')
    # print(v)

'''
def test_db():
    sql = "INSERT INTO `guest`.`sign_guest`(`realname`, `phone`, `email`, `sign`, `event_id`) " \
          "VALUES ('wowo', '18331310101', 'wowo@mail.com', 0, 1);"
    db = MyDB()
    execute_sql = db.execute_sql(sql)
    print(execute_sql)
    db.close_db()



def get_xlsx():
    """ 从接口文档获取测试数据，包括sql """
    case_path = r'/testFile/case_data/case_guest.xlsx'
    a = App(visible=False, add_book=False)
    wb = a.books.open(case_path)
    sheet = wb.sheets['sheet1']
    case_list = []
    try:
        # 获取sheet1内数据的范围，返回元组
        ran = sheet.used_range.shape
        # 遍历excel内所有数据，每行作为一条用例存放于case_list
        for r in range(ran[0] - 1):
            # 判断用例是否需要执行，不需要则跳过
            if sheet[r + 1, 7] is None or sheet[r + 1, 7].value in ['n', 'N']:
                continue
            case = []
            for l in range(ran[1] - 2):
                # sheet[r + 1, l + 1] 从A3开始取数据，空单元格默认赋值 None，避免xlwings丢失空单元格数据
                if sheet[r + 1, l + 2] is None:
                    case.append(None)
                else:
                    case.append(sheet[r + 1, l + 2].value)
            case_list.append(case)
    finally:
        wb.close()
        a.quit()
    return case_list


def find_c():
    for c in get_xlsx():
        return c


class BB:
    def __init__(self):
        print('BB放在类外面')

    @staticmethod
    def b():
        print("这是外面的b方法")


# bbb = BB()
cl = get_xlsx()
'''

@ddt
class AA(unittest.TestCase):
    aaa = 'aaa放在类里面'

    def setParameters(self, name):
        self.name = name

    @classmethod
    def setUpClass(cls) -> None:
        print('setUpClass：')

    def setUp(self) -> None:
        print('setUp：')

    @data('用例1', '华为')
    def test_1(self, ppa):
        """
        used ddt test
        :param ppa:
        :return:
        """
        print('用例1 %s' % ppa)

    def tearDown(self) -> None:
        print('tearDown：')

    @classmethod
    def tearDownClass(cls) -> None:
        print('tearDownClass：')


if __name__ == '__main__':
    # xlwings_read()
    # send_request()
    # print(time.time())
    # test_db()
    '''
    a = [[1, 2], ['a', 'b']]
    b = map(lambda x: x, a)
    print(b.__next__())
    print(b.__iter__())
    '''
    # case_list = get_xlsx('case_guest.xlsx')
    fp = open(r'D:\Program Files\JetBrains\Projects\pythonProjects\interfaceTest\testCase\aaa\report.html', 'wb+')
    s_dir = r'D:\Program Files\JetBrains\Projects\pythonProjects\interfaceTest\testCase\aaa'
    suite = unittest.defaultTestLoader.discover(start_dir=s_dir)
    runner = HTMLTestRunner(fp)
    runner.run(suite)
    fp.close()
