import django.utils.timezone as timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta


# Create your models here.

class UserProfile(AbstractUser):
    # buildingCode - the code for which building you lived in
    buildingCode = models.CharField(max_length=20, verbose_name='楼号')
    floorCode = models.CharField(max_length=20, verbose_name='层号')
    roomCode = models.CharField(max_length=20, verbose_name='房号')

    class Meta:
        db_table = 'Users'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class EmailVeriRecord(models.Model):
    # verification code
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='用户邮箱')
    send_time = models.DateTimeField(default=timezone.localtime(), verbose_name='发送时间', null=True, blank=True)
    expire_time = models.DateTimeField(default=timezone.localtime()+timedelta(minutes=10) + timedelta(minutes=10), verbose_name='过期时间',
                                       null=True)
    email_type = models.CharField(max_length=10, choices=(('register', '注册'), ('forget', '找回')))

    class Meta:
        verbose_name = '邮箱验证'
        verbose_name_plural = verbose_name
