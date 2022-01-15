from django.db import models
from django.db.models import constraints

from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, db_column='UID', verbose_name='username', unique=True)
    password = models.CharField(max_length=200, db_column='PW', verbose_name='password')
    email = models.EmailField(max_length=50, db_column='EMAIL',verbose_name='email')
    
    def __str__(self):
            return self.username
    
    
    class Meta:
        # proxy = True
        db_table = 'user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자 리스트'
        ordering = ('username',)


class Device(models.Model):
    serial = models.CharField(db_column='Serial_ID', max_length=100, verbose_name='시리얼 번호', help_text='This value is automatically entered by reference.')
    master = models.ForeignKey(CustomUser, db_column='Master', verbose_name='마스터', related_name='master', on_delete=models.CASCADE, default='')
    nickname = models.CharField(db_column='Nickname',verbose_name='기기 닉네임', default='닉네임 없음', max_length=30 )
    created_at = models.DateTimeField(db_column='CRE_DT', verbose_name='생성 날짜', help_text='This value is automatically entered when the table is created.', auto_now_add=True, null=True, blank=True)
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
    device = models.ForeignKey(Device, db_column='Device', verbose_name='디바이스 id', related_name='device',on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, db_column='User', verbose_name='유저 id', related_name='user',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'Guest'
        verbose_name = '게스트'
        verbose_name_plural = '게스트 리스트'

# Not complete
class History(models.Model):
    user= models.OneToOneField(CustomUser, db_column='UID', verbose_name='소유자', help_text='This value is automatically entered when the table is created.', on_delete=models.CASCADE)
    created_at = models.DateTimeField(db_column='CRE_DT', verbose_name='생성 날짜', help_text='This value is automatically entered when the table is created.', auto_now_add=True, null=True, blank=True)
    device = models.OneToOneField(Device, db_column='Device_ID',verbose_name='디바이스 시리얼 번호', help_text='This value is automatically entered when the table is created.',on_delete=models.CASCADE, default='')
    mode = models.CharField(db_column='Mode_ST', verbose_name='디바이스 모드', help_text='If the state is normal N is if the the state is emergency F is automatically entered.', max_length=1, default='N', )
    latitude = models.FloatField(db_column='Latitude_ST', verbose_name='위도', help_text='This value is automatically entered by receiving the status of the connected device',default=0.0 )
    longitude = models.FloatField(db_column='longitude_ST', verbose_name='경도', help_text='This value is automatically entered by receiving the status of the connected device', default=0.0)
    altitude = models.FloatField(db_column='altitude_ST', verbose_name='고도', help_text='This value is automatically entered by receiving the status of the connected device', default=0.0)
    ONF = models.BooleanField(db_column='ONF_ST', verbose_name='디바이스 On/Off', help_text='This vaule is automatically entered by receiving the status of the connected device', default=True)
    IP = models.GenericIPAddressField(db_column='IP_INFO', verbose_name='IP', null=True)
    
    def __str__(self):
        return '%s 디바이스의 이전 기록' % (self.user)
    
    class Meta:
        # unique_together = (('user_id', 'created_time'),)
        db_table = 'history_info'
        verbose_name = '이전 기록'
        verbose_name_plural = '이전 기록 리스트'
        constraints = [
            models.UniqueConstraint(
                fields=['created_at', 'user', 'device'],
                name = 'unique history',
                # deferrable = constraints.Deferrable.DEFERRED,
            )
        ]
        
        
        
class City_CSV(models.Model):
    name = models.CharField(max_length=20, db_column='CITY_NAME')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'City'
        verbose_name = '시'
        verbose_name_plural = '시 리스트'
        
    
class Country_CSV(models.Model):
    name = models.CharField(max_length=20, db_column='COUNTRY_NAME')
    city = models.ForeignKey('City_CSV', on_delete=CASCADE, db_column='CITY', default='city')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Country'
        verbose_name = '구'
        verbose_name_plural = '구 리스트'
        
        

class District_CSV(models.Model):
    name = models.CharField(max_length=20, db_column='DISTRICT_NAME')
    country = models.ForeignKey('Country_CSV', on_delete=CASCADE, db_column='COUNTRY', default='country')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'District'
        verbose_name = '동'
        verbose_name_plural = '동 리스트'
        
        


class DistrictWhiteList(models.Model):
    device = models.ForeignKey(Device, db_column='Device', verbose_name='디바이스', related_name='white_list_device', on_delete=models.CASCADE)
    white_list = models.ForeignKey(District_CSV, db_column='WhiteList', verbose_name='안심지역', related_name='list', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'DistrictWhiteList'
        verbose_name = '안심지역'
        verbose_name_plural = '안심지역 리스트'
