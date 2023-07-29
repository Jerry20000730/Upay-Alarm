from django.core.mail import send_mail
from upay_alarm_backend.models import EmailVeriRecord
import random
import datetime
from upay_alarm_V1 import settings


def veri_code():
    # generate all possibilities
    code = '%06d' % random.randint(0, 999999)

    code_str = str(code)
    return code_str


def send_email(desc_email, send_type='register'):
    email = EmailVeriRecord()
    # randomly generate verification code
    email.code = veri_code()

    # specify email recipient
    email.email = desc_email

    # specify sending time
    email.send_time = datetime.datetime.now()

    # specify expiring time
    email.expire_time = datetime.datetime.now() + datetime.timedelta(minutes=10)

    # specify if the email is for registration or forgetting the password
    email.email_type = send_type

    # send email
    try:
        if send_type == 'register':
            send_status = send_mail(
                subject="[upay_alarm] 验证您的邮箱 Verify Your Email Address",
                message="尊敬的用户您好：\n\n        感谢您注册upay_alarm，请确认以下注册信息无误：\n\n        您的注册邮箱为：{}\n        您的验证码为：{}\n\n        此邮件为自动发送，如果您发现您并没有注册本服务，请主动忽略此邮件；请勿回复此邮件，感谢配合！\n\nDear user, \n        Thank you for registering the upay_alarm, please check the following information due to potential security issues:\n\n        Registration email: {}\n        Verification code: {}\n\n        This is an automatic email, if you did not register for this service, please kindly ignore this email. Please do not reply to this email. Thank you for your cooperation. \n\nKind regards,\nupay_alarm".format(desc_email, email.code, desc_email, email.code),
                from_email=settings.EMAIL_FROM,
                recipient_list=[desc_email],
            )
            if send_status:
                # save email record
                email.save()
                return True
            else:
                return False
        elif send_type == 'forget':
            send_status = send_mail(
                subject="[upay_alarm] 找回密码 Forget Your Password?",
                message="尊敬的用户您好：\n        我们会帮助你找回密码，请点击下方链接重置密码。\n        localhost/reset/{}\n        此邮件为自动发送，请勿回复此邮件，感谢配合！\nDear user,\n        We will help you reset your password, please check the following URL to reset your password: \n        localhost/reset/{}\n        This is an automated email, please do not reply to this email. Thank you for your cooperation. \nRegards,\nupay_alarm".format(email.code, email.code),
                from_email=settings.EMAIL_FROM,
                recipient_list=[desc_email]
            )
            if send_status:
                # save email record
                email.save()
                return True
            else:
                return False
    except EmailVeriRecord as e:
        print(e)
        return False


