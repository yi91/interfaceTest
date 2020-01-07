# coding:utf-8

import requests
import readConfig
import os
from xlrd import open_workbook
from xml.etree import ElementTree
from common.Log import MyLog as Log
import json
import base64

localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
log = Log.get_log()
logger = log.get_logger()


def my_base64(string):
    """ 定义auth的加密方法
    base64.b64encode(string.encode('utf-8'))得到的是byte类型str，b'YWJjcjM0cjM0NHI='
    只想要获得YWJjcjM0cjM0NHI=，再将byte转换回去就好了
    """
    return str(base64.b64encode(string.encode('utf-8')), 'utf-8')


def get_visitor_token():
    """
    create a token for visitor
    :return:
    """
    scheme = localReadConfig.get_http("SCHEME")
    host = localReadConfig.get_http("BASEURL")
    response = requests.get(scheme + '://' + host + "/v2/User/Token/generate")
    info = response.json()
    token = info.get("info")
    logger.debug("Create token:%s" % (token))
    return token


def set_visitor_token_to_config():
    """
    set token that created for visitor to config
    :return:
    """
    token_v = get_visitor_token()
    localReadConfig.set_headers("TOKEN_V", token_v)


def get_value_from_return_json(json, name1, name2):
    """
    get value by key
    :param json:
    :param name1:
    :param name2:
    :return:
    """
    info = json['info']
    group = info[name1]
    value = group[name2]
    return value


def show_return_msg(response):
    """
    show msg detail
    :param response:
    :return:
    """
    url = response.url
    msg = response.text
    print("\nresponse：\n请求地址：" + url)
    # 可以显示中文
    print("请求返回值：" + '\n' + json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4) + '\n')


# ****************************** 从excel文件中读取测试用例 ********************************
def get_xls(xls_name, sheet_name):
    """
    get interface data from xls file
    :return:
    """
    cls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    # open xls file
    file = open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    # 遍历里每一行
    for i in range(nrows):
        # 如果不是标题行，就加入到列表
        if sheet.row_values(i)[0] != u'case_name':
            # 如果是表格内容是文本格式，得到的就是str，数字格式得到的就是float
            cls.append(sheet.row_values(i))
    return cls


# ****************************** 从xml文件中读取sql语句 ********************************
def set_xml():
    """
    获取所有的数据库、表信息并转成字典格式
    :return:
    """
    database = {}

    if len(database) == 0:
        sql_path = os.path.join(proDir, "testFile", "SQL.xml")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            # print(db_name)
            table = {}
            for tb in list(db):
                table_name = tb.get("name")
                # print(table_name)
                sql = {}
                for data in list(tb):
                    sql_id = data.get("id")
                    # print(sql_id)
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table
    return database


def get_xml_dict(database_name, table_name):
    """
    获取指定数据库和指定表的所有集合
    :param database_name:
    :param table_name:
    :return:
    """
    database = set_xml()
    sqls_dic = database.get(database_name).get(table_name)
    # 返回所有的sql
    return sqls_dic


def get_sql(database_name, table_name, sql_id):
    """
    通过name和id获取指定的sql
    :param database_name:
    :param table_name:
    :param sql_id:
    :return:
    """
    sqls_dic = get_xml_dict(database_name, table_name)
    sql = sqls_dic.get(sql_id)
    return sql


# ****************************** 从xml文件中读取接口url ********************************
def get_url_from_xml(name):
    """
    By name get url from interfaceURL.xml
    :param name: interface's url name
    :return: url
    """
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in list(u):
                url_list.append(c.text)

    # xml文件获取的url_list不能为空（None）
    if url_list.count(None) > 0:
        logger.info("url的xml文件有字段为空！！！")

    # 遍历去掉None对象
    for i in url_list:
        if i is None:
            url_list.remove(i)
    # /v2/ + group + module + action
    url = '/' + '/'.join(url_list) + '/'
    return url


if __name__ == "__main__":
    print(get_xls("apiCase.xlsx", 'sec_get_event_list'))
    # print(get_url_from_xml('bloglogin'))
