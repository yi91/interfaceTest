import json

import requests
from requests.auth import HTTPBasicAuth
from xlwings import App
import common.common_def as cd
from common.read_config import ReadConfig
import datetime, time

case = []
path = r'D:\Program Files\JetBrains\Projects\pythonProjects\interfaceTest\testFile\case_data\case_template.xlsx'


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

    # cd.write_resp_to_excel('case_template.xlsx', 'test_users_auth_error', resp)


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
    v = cd.get_value_from_response(json.dumps(jo, ensure_ascii=False), 'token')
    print(v)


if __name__ == '__main__':
    # xlwings_read()
    send_request()
    # print(time.time())

