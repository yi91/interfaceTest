# coding:utf-8

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
from common.read_config import ReadConfig
from common.logger import MyLog

rc = ReadConfig()
rp = rc.get_report()
logger = MyLog.logger('Email')
pro_dir = os.path.dirname(os.path.dirname(__file__))


class Email:
    def __init__(self):
        self.host = rc.get_email("mail_host")
        self.port = rc.get_email("mail_port")
        self.user = rc.get_email("mail_user")
        self.password = rc.get_email("mail_pass")

        self.sender = rc.get_email("sender")
        self.title = rc.get_email("subject")
        self.content = rc.get_email("content")

        # get receiver list，另外接收者带上自己
        self.value = rc.get_email("receiver")
        self.receivers = [self.sender]
        for r in str(self.value).split("/"):
            self.receivers.append(r)
        logger.info('收件人：%r' % self.receivers)

        # 采用related定义内嵌资源的邮件实例，即带附件的邮件。multipart类型主要有三种子类型：mixed、alternative、related
        self.msg = MIMEMultipart('related')

        # 定义邮件的主题
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.subject = "接口测试报告 " + date
        logger.info('邮件主题：%s' % self.subject)

    def config_header(self):
        """ defined email header include subject, sender and receiver """
        self.msg['subject'] = self.subject
        self.msg['from'] = self.sender
        self.msg['to'] = ";".join(self.receivers)

    def config_content(self):
        """ 定义邮正文内容，MIMEText()用于定义邮件正文，参数为内容的格式， plain代表简单的文本格式"""

        # with open(os.path.join(readConfig.proDir, 'testFile', 'emailStyle.txt')) as f:
        #     content = f.read()
        # content_plain = MIMEText(content, 'html', 'utf-8')

        # 使用简单的文本作为邮件正文内容
        content_plain = MIMEText('测试报告，请查收...', 'plain', 'utf-8')
        self.msg.attach(content_plain)

        # 添加图片作为内容
        # self.config_image()

    def config_image(self):
        """ 定义插入邮件正文的图片 """
        image_path = os.path.join(pro_dir, 'testFile', 'img', 'report.png')
        with open(image_path, 'rb') as fp:
            msg_image = MIMEImage(fp.read())

        # 定义图片的id，在邮件正文（或者html）中引用
        msg_image.add_header('Content-ID', '<image1>')
        self.msg.attach(msg_image)

    def config_file(self):
        """ 构造附件 """
        if self.check_file():
            '''
            # 压缩文件得到zip包
            zippath = os.path.join(testCase.runAll.proDir, "report", "test.zip")
            files = glob.glob(rp + '\*')
            f = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
            for file in files:
                # 修改压缩文件的目录结构
                f.write(file, '/report/'+os.path.basename(file))
            f.close()
            '''

            with open(rp + 'report.html', 'rb')as r:
                fh = MIMEText(str(r.read()), 'base64', 'utf-8')
            fh['Content-Type'] = 'application/octet-stream'
            fh['Content-Disposition'] = 'report.html'
            self.msg.attach(fh)

            with open(rp + 'output.log', 'rb')as o:
                ol = MIMEText(str(o.read()), 'base64', 'utf-8')
            ol['Content-Type'] = 'application/octet-stream'
            ol['Content-Disposition'] = 'output.log'
            self.msg.attach(ol)

    @staticmethod
    def check_file():
        """ 检查测试报告是否存在 """
        if os.path.isfile(rp + 'report.html') and not os.stat(rp) == 0:
            return True
        else:
            logger.error('测试报告不存在，请检查')
            return False

    def send_email(self):
        logger.info('准备发邮件')
        self.config_header()
        self.config_content()
        self.config_file()
        # host可以是qq或者163的服务器地址，端口一般默认465，smtplib.SMTP_SSL(host, port)
        smtp = smtplib.SMTP_SSL('smtp.163.com', 465)
        try:
            # password必须是授权码
            smtp.login(self.user, self.password)
            smtp.sendmail(self.sender, self.receivers, self.msg.as_string())
            logger.info("The test report has send to developer by email.")
        except Exception as ex:
            logger.error('邮件发送失败，请检查 \n %s' % ex.args)
        finally:
            smtp.quit()


'''
class MyEmail:
    email = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_email():

        if MyEmail.email is None:

            MyEmail.mutex.acquire()
            # 关联MyEmail和Email的对象
            MyEmail.email = Email()
            MyEmail.mutex.release()

        return MyEmail.email
'''

if __name__ == "__main__":
    Email().send_email()
