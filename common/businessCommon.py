# coding:utf-8

from common import configHttp, commondef
import readConfig

# 业务分离

localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localLogin_xls = commondef.get_xls("userCase.xlsx", "login")
localAddAddress_xls = commondef.get_xls("userCase.xlsx", "addAddress")


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


