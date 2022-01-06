from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models import constraints
from django.db.models.fields import related

class CustomUser(AbstractUser):

    username = models.CharField(max_length=100, db_column='UID', verbose_name='username', unique=True)
    password = models.CharField(max_length=200, db_column='PW', verbose_name='password')
    email = models.EmailField(max_length=50, db_column='EMAIL',verbose_name='email')
    
    def __str__(self):
            return self.username
    
    class Meta:
        proxy = True
        db_table = 'user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자 리스트'
        ordering = ('username',)


class Device(models.Model):
    serial = models.CharField(db_column='Serial_ID', verbose_name='시리얼 번호', help_text='This value is automatically entered by reference.')
    master = models.ForeignKey(CustomUser, db_column='Master', verbose_name='마스터', related_name='master')
    nickname = models.CharField(db_column='Nickname',verbose_name='기기 닉네임', default='닉네임 없음', max_length=30 )
    def __str__(self):
            return self.serial
    
    class Meta:
        db_table = 'Device'
        verbose_name = '디바이스'
        verbose_name_plural = '디바이스 리스트'
        constraints = [
            models.UniqueConstraint(
                fields=['serial',],
                name = 'unique device',
                # deferrable = constraints.Deferrable.DEFERRED,
            )
        ]

class Guest(models.Model):
    device = models.ForeignKey(Device, db_column='Device', verbose_name='디바이스 id', related_name='device')
    user = models.ForeignKey(CustomUser, db_column='User', verbose_name='유저 id', related_name='user')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'Guest'
        verbose_name = '게스트'
        verbose_name_plural = '게스트 리스트'



    
