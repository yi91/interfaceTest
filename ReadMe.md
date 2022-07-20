注意：excel增减字段，对应需要修改的方法：write_resp_to_excel()/get_xlsx()，还有测试用例字段初始化也需要修改

新项目操作步骤：

1、config.ini配置好 [DATABASE] 信息和 [HTTP] 的 base_url 信息

2、testFile/case_data下新建接口的xlsx表格

3、testCase下按项目名，写用例，可以复制test_all_case，
只需修改case_list = cc.get_xlsx('case_django_rest.xlsx') 和 
cc.write_resp_to_excel('case_django_rest.xlsx', self.case_name, self.r, self.msg)
