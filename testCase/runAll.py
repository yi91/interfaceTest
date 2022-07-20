# coding:utf-8

import os
import unittest
from datetime import datetime
from XTestRunner import HTMLTestRunner
from common.read_config import ReadConfig
rc = ReadConfig()
# 创建 report_path
proDir = os.path.dirname(os.path.dirname(__file__))
report_path = proDir + "\\report\\%s\\" % str(datetime.now().strftime("%Y%m%d%H%M%S"))
if not os.path.exists(report_path):
    os.mkdir(report_path)
    rc.set_report(report_path)

# 此行导包代码必须放在创建 report_path 下面，确保其他代码获取到的 report_path 是最新的路径
from common.config_email import Email


class AllTest:
    def __init__(self):
        # 是否开启邮件发送
        on_off = rc.get_email("on_off")
        self.email = Email()


"""

            # send test report by email
            if on_off == 'on':
                self.email.send_email()
                print('\n邮件发送成功！')
            elif on_off == 'off':
                logger.info("Doesn't send report email to developer.")
            else:
                logger.info("Unknow state.")
"""


if __name__ == '__main__':
    # 初始化测试数据
    # businessCommon.init_test_data()

    # obj = AllTest()
    # obj.run()

    # 测试完成删除测试数据
    # businessCommon.del_init()
    suit = unittest.TestLoader().discover(start_dir='api_guest', top_level_dir=proDir)
    # 必须 wb 打开方式
    with open(report_path + 'report.html', 'wb+') as fp:
        runner = HTMLTestRunner(fp, title='Test Report', description='Test Description')
        runner.run(suit)

'''
用例执行的顺序
my_unittest 框架默认根据ASCII码的顺序加载测试用例，数字与字母的顺序为：0~9，A~Z,a~z 
如果要让某个测试用例先执行，不能使用默认的main()方法，需要通过TestSuite类的addTest（）方法按照一定的顺序来加载

过程：caselist文件--->testCase目录--->discover--->testBloglLogin--->Testxxx()
'''
