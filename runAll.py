# coding:utf-8

import os
import unittest
from common.Log import MyLog as Log
from common import HTMLTestRunner, businessCommon
import readConfig
from common.configEmail import MyEmail

localReadConfig = readConfig.ReadConfig()


class AllTest:
    def __init__(self):
        global log, logger, resultPath, on_off

        log = Log.get_log()
        logger = log.get_logger()
        resultPath = log.get_report_path()
        # 是否开启邮件发送
        on_off = localReadConfig.get_email("on_off")

        self.caseListFile = os.path.join(readConfig.proDir, "caselist.txt")
        self.caseFile = os.path.join(readConfig.proDir, "testCase")
        # self.caseFile = None
        self.caseList = []
        self.email = MyEmail.get_email()

    def set_case_list(self):
        """
        set case list
        :return:
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            # 过滤掉caselist文件中#注释的
            if data != '' and not data.startswith("#"):
                self.caseList.append(data.replace("\n", ""))
        fb.close()

    def set_case_suite(self):
        """
        set case suite
        :return:
        """
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_module = []

        for case in self.caseList:
            case_name = case.split("/")[-1]
            print(case_name+".py")
            '''
            discover(start_dir,pattern='test*.py',top_level_dir=None)
                start_dir：要测试的模块名或测试用例的目录
                pattern：表示用例文件名的匹配原则，默认test*.py的文件，重写pattern可以覆盖
                top_level_dir=None ：测试模块的顶层目录，如果没有顶层目录，默认为None
            '''
            # start_dir定的位置过高，会导致suite_module存在过多空testsuite
            start_dir = self.caseFile + '\\' + case.split("/")[0]
            discover = unittest.defaultTestLoader.discover(start_dir, pattern=case_name + '.py', top_level_dir=None)
            suite_module.append(discover)

        if len(suite_module) > 0:
            # 注意层级
            for disc in suite_module:
                for suite in disc:
                    for test_case in suite:
                        test_suite.addTests(test_case)
        else:
            return None

        return test_suite

    def run(self):
        """
        run test
        :return:
        """
        fp = open(resultPath, 'wb')
        try:
            suit = self.set_case_suite()
            if suit is not None:
                logger.info("********TEST START********")
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')
                runner.run(suit)
            else:
                logger.info("Have no case to test.")
        except Exception as ex:
            logger.error(str(ex))
        finally:
            logger.info("*********TEST END*********")
            # 注意fp需要提前声明
            fp.close()

            # send test report by email
            if on_off == 'on':
                self.email.send_email()
                print('\n邮件发送成功！')
            elif on_off == 'off':
                logger.info("Doesn't send report email to developer.")
            else:
                logger.info("Unknow state.")


if __name__ == '__main__':
    # 初始化测试数据
    businessCommon.init_test_data()

    obj = AllTest()
    obj.run()

    # 测试完成删除测试数据
    # businessCommon.del_init()

'''
用例执行的顺序
my_unittest 框架默认根据ASCII码的顺序加载测试用例，数字与字母的顺序为：0~9，A~Z,a~z 
如果要让某个测试用例先执行，不能使用默认的main()方法，需要通过TestSuite类的addTest（）方法按照一定的顺序来加载

过程：caselist文件--->testCase目录--->discover--->testBloglLogin--->Testxxx()
'''
