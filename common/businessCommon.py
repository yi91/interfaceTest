# coding:utf-8

from common import configHttp, commondef, configDB
import readConfig

# 业务分离
from common.configDB import MyDB

localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localLogin_xls = commondef.get_xls("userCase.xlsx", "login")
localAddAddress_xls = commondef.get_xls("userCase.xlsx", "addAddress")
localConfigDB = configDB.MyDB()


# login
def login():
    """
    login
    :return: token
    """
    # set url
    url = commondef.get_url_from_xml('login')
    localConfigHttp.set_url(url)

    # set header
    token = localReadConfig.get_headers("token_v")
    header = {"token": token}
    localConfigHttp.set_headers(header)

    # set param
    data = {"email": localLogin_xls[0][3],
            "password": localLogin_xls[0][4]}
    localConfigHttp.set_data(data)

    # login
    response = localConfigHttp.post().json()
    token = commondef.get_value_from_return_json(response, "member", "token")
    return token


# logout
def logout(token):
    """
    logout
    :param token: login token
    :return:
    """
    # set url
    url = commondef.get_url_from_xml('logout')
    localConfigHttp.set_url(url)

    # set header
    header = {'token': token}
    localConfigHttp.set_headers(header)

    # logout
    localConfigHttp.get()


# 初始化insert event数据
def init_test_data():
    # create data
    datas = {
        'sign_event': [
            (1, '红米Pro发布会', 2000, 1, '北京会展中心', '2017-08-20 14:00:00', '2018-07-10 14:00:00'),
            (2, '可参加人数为0', 0, 1, '北京会展中心', '2017-08-20 14:00:00', '2018-07-10 14:00:00'),
            (3, '当前状态为0关闭', 2000, 0, '北京会展中心', '2017-08-20 14:00:00', '2018-07-10 14:00:00'),
            (4, '发布会已结束', 2000, 1, '北京会展中心', '2001-08-20 14:00:00', '2018-07-10 14:00:00'),
            (5, '小米5发布会', 2000, 1, '北京国家会议中心', '2017-08-20 14:00:00', '2018-07-10 14:00:00')
        ],
        'sign_guest': [
            (1, 'alen', 13511001100, 'alen@mail.com', 0, 1, '2017-08-20 14:00:00'),
            (2, 'hasign', 13511001101, 'hsign@mail.com', 1, 1, '2017-08-20 14:00:00'),
            (3, 'tom', 13511001102, 'tom@mail.com', 0, 5, '2017-08-20 14:00:00')
        ],
    }

    event_sql = commondef.get_sql('guest', 'sign_event', 'insert_event')
    guest_sql = commondef.get_sql('guest', 'sign_guest', 'insert_guest')

    sql = ''
    try:
        for table, data in datas.items():
            if table == 'sign_event':
                sql = event_sql
            elif table == 'sign_guest':
                sql = guest_sql

            for d in data:
                localConfigDB.executeSQL(sql, d)
                # 查看执行完之后的游标是否不为空
                if localConfigDB.cursor is not None:
                    print("初始化event数据成功")
    finally:
        localConfigDB.closeDB()


def del_init():
    """ 删除测试数据 """
    event_id = [1, 2, 3, 4, 5]
    del_event = commondef.get_sql('guest', 'sign_event', 'delete_event')

    guest_id = [1, 2, 3]
    del_guest = commondef.get_sql('guest', 'sign_guest', 'delete_guest')

    try:
        localConfigDB.executeSQL('SET FOREIGN_KEY_CHECKS=0;', None)
        for i in event_id:
            localConfigDB.executeSQL(del_event, (i, ''))
        for r in guest_id:
            localConfigDB.executeSQL(del_guest, (r, ''))
    finally:
        localConfigDB.closeDB()

