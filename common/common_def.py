# coding:utf-8
import os
import json
import base64
import re
import time
import requests
from xlwings import App
from common.logger import Log
from common.read_config import ReadConfig


rc = ReadConfig()
logger = Log('common_def').get_logger()
pro_dir = os.path.dirname(os.path.dirname(__file__))


def my_base64(string):
    """ 定义auth的加密方法
    base64.b64encode(string.encode('utf-8'))得到的是byte类型str，b'YWJjcjM0cjM0NHI='
    只想要获得YWJjcjM0cjM0NHI=，再将byte转换回去就好了
    """
    return str(base64.b64encode(string.encode('utf-8')), 'utf-8')


def get_token():
    """ 获取接口需要的token """
    token = rc.get_header('token')
    tt = rc.get_header('token_time')
    allow_time = time.time() - float(tt)
    # 如果token的有效期超过24小时，就获取新的token
    if allow_time > 24*60*60*1000:
        resp = requests.get(rc.get_http('token_url'))
        token = get_value_from_response(resp, 'token')
        # 写入配置文件
        rc.set_header("token", token)
        rc.set_header('token_time', time.time())
        logger.info('已将新获取的 token 写入配置文件')
    logger.info("获取 token 成功：%s" % token)
    return token


def get_value_from_response(response, kwarg):
    """ 从接口返回值中获取需要的字段内容 """
    re_str = r'"%s": "(.+?)"' % kwarg
    # 利用正则匹配后，获取列表的第一个元素
    value = re.findall(re_str, response.text)[0]
    logger.info('获取断言内容为：%s' % value)
    return value


def show_return_msg(response):
    # 格式化输出response内容
    logger.info("response的请求地址：%s" % response.url)
    # ensure_ascii=False告诉python不用把中文转成Unicode
    logger.info("请求返回值：\n", json.dumps(response.json(), ensure_ascii=False, sort_keys=True, indent=4,
                                       separators=(',', ':')) + '\n')


def write_resp_to_excel(xlsx_name, case_name, response, msg):
    case_path = os.path.join(pro_dir, "testFile", 'case_data', xlsx_name)
    if os.path.exists(case_path):
        a = App(visible=False, add_book=False)
        wb = a.books.open(case_path)
        sheet = wb.sheets['sheet1']
        ran = sheet.used_range.shape
        try:
            # 遍历excel内所有数据，每行作为一条用例存放于测试结果和response
            for r in range(ran[0] - 1):
                # 找到正在测试的用例名称
                if sheet[r + 1, 1].value.lower() == case_name:
                    # 必须先判断response为null的情况
                    if response is None:
                        # 任何错误导致的response为null，都当请求失败处理
                        sheet[r + 1, 7].value = 'fail'
                        sheet[r + 1, 8].value = '请求参数有误，返回值是None'
                        logger.info('接口测试失败，请检查 excel 内的 response')
                    # 判断状态码和断言信息
                    elif response.status_code == 200 and (msg in response.text):
                        sheet[r + 1, 7].value = 'success'
                        sheet[r + 1, 8].value = response.text
                        logger.info('接口测试成功，结果和返回值已写入 excel ')
                    else:
                        sheet[r + 1, 7].value = 'fail'
                        sheet[r + 1, 8].value = response.text
                        logger.info('断言失败，请检查 excel 内的 response')
                    # 一旦找到，跳出循环
                    break
        finally:
            wb.save()
            wb.close()
            a.quit()
    else:
        logger.info('测试用例excel名称填写错误，请检查')


# ******************** 从excel文件中读取测试用例 ***********************
def get_xlsx(xlsx_name):
    """ 从接口文档获取测试数据，包括sql """
    case_list = []
    # 用例路径
    case_path = os.path.join(pro_dir, "testFile", 'case_data', xlsx_name)
    if os.path.exists(case_path):
        # 初始化excel操作对象
        app = App(visible=False, add_book=False)
        wb = app.books.open(case_path)
        try:
            sheet = wb.sheets['sheet1']
            # 获取sheet1内数据的范围，返回元组
            ran = sheet.used_range.shape
            # 遍历excel内所有数据，每行作为一条用例存放于case_list
            for r in range(ran[0] - 1):
                # 如果用例不需要执行，则跳过
                if sheet[r + 1, 6] is None or sheet[r + 1, 6].value.lower() == 'n':
                    continue
                case = []
                for l in range(ran[1] - 1):
                    # sheet[r + 1, l + 1] 从A2开始取数据，空单元格默认赋值 None，避免xlwings丢失空单元格数据
                    if sheet[r + 1, l + 1] is None:
                        case.append(None)
                    else:
                        case.append(sheet[r + 1, l + 1].value)
                case_list.append(case)
            logger.info('读取 %s 用例成功' % xlsx_name)
        except Exception as e:
            logger.error('读取用例数据失败，请检查excel用例的编写规范', e)
        finally:
            wb.close()
            app.quit()
    else:
        logger.info('测试用例excel名称填写错误，请检查')

    return case_list


if __name__ == "__main__":
    print(get_xlsx("apiCase.xlsx"))
    # print(get_url_from_xml('bloglogin'))
