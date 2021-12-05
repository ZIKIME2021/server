from django.db import models
from django.contrib.auth.models import User
from django.db.models import constraints

# Master, Guest 모두 CustomUser 모델
class CustomUser(User):
    
    def __str__(self):
            return self.username
    
    class Meta:
        proxy = True
        db_table = 'user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자 리스트'
        ordering = ('username',)
        
        
# 서비스하는(=판매된) 기기들의 시리얼 정보를 모두 저장
class Serial(models.Model):
    serial_number = models.CharField(db_column='SerialID', unique=True, max_length=50, verbose_name='시리얼 번호', help_text='This serial number must be unique.')
    created_at = models.DateTimeField(db_column='CRE_DT', verbose_name='생성 날짜', help_text='This value is entered automatically.', null=True, blank=True, auto_now_add=True)
    deleted_at = models.DateTimeField(db_column='DEL_DT', verbose_name='만료 날짜', help_text='If you enter the date here, this device will no longer be available.', auto_now=True, null=True, blank=True)
   
    def __str__(self):
            return self.serial_number
        
    class Meta:
        db_table = 'serial_info'
        verbose_name = '시리얼'
        verbose_name_plural = '시리얼 리스트'
        
        
# 디바이스의 serial, Master 필드는 모두 foreign key
# 기기등록시, server는 qt-iot에서 받아온 모듈 정보도 같이 저장해줘야함.
class Device(models.Model):
    serial = models.OneToOneField(Serial, db_column='Serial_ID', verbose_name='시리얼 번호', help_text='This value is automatically entered by reference.',on_delete=models.CASCADE)
    gps_module_info = models.CharField(db_column='GPS_INFO', verbose_name='GPS 모듈 정보', help_text='This value is automatically entered by device connecting.', max_length=100)
    camera_module_info = models.CharField(db_column='CAMERA_INFO', verbose_name='카메라 모듈 정보', help_text='This value is automatically entered by device connecting.', max_length=100)
    created_at = models.DateTimeField(db_column='CRE_DT', verbose_name='디바이스 등록 날짜', help_text='This value is automatically entered when the table is created.',auto_now_add=True,  null=True)
   
    def __str__(self):
            return self.serial.serial_number
    
    class Meta:
        db_table = 'device_info'
        verbose_name = '디바이스'
        verbose_name_plural = '디바이스 리스트'
        constraints = [
            models.UniqueConstraint(
                fields=['serial'],
                name = 'unique device',
                # deferrable = constraints.Deferrable.DEFERRED,
            )
        ]
        
        
# Device 레코드 생성 시, 기기 상태 정보를 가지고 있는 Status 레코드도 생성해줘야함.
# device 
# 0 0 1 00 30 69 ....
# 1 0 1 01 30 69 ...
# ..
# Select latitude From status where 
class Status(models.Model):
    device = models.ForeignKey(Device, db_column='Device_ID',verbose_name='디바이스 시리얼 번호', help_text='This value is automatically entered when the table is created.',on_delete=models.CASCADE, default='')
    mode = models.CharField(db_column='Mode_ST', verbose_name='디바이스 모드', help_text='If the state is normal N is if the the state is emergency F is automatically entered.', max_length=1, default='N', )
    latitude = models.FloatField(db_column='Latitude_ST', verbose_name='위도', help_text='This value is automatically entered by receiving the status of the connected device',default=0.0 )
    longitude = models.FloatField(db_column='longitude_ST', verbose_name='경도', help_text='This value is automatically entered by receiving the status of the connected device', default=0.0)
    altitude = models.FloatField(db_column='altitude_ST', verbose_name='고도', help_text='This value is automatically entered by receiving the status of the connected device', default=0.0)
    latest_updated_at= models.DateTimeField(db_column='UDA_DT', verbose_name='최근 업데이트한 시간', help_text='This value is automatically entered when the table is updated.', auto_now=True)
    ONF = models.BooleanField(db_column='ONF_ST', verbose_name='디바이스 On/Off', help_text='This vaule is automatically entered by receiving the status of the connected device', default=True)
    IP = models.GenericIPAddressField(db_column='IP_INFO', verbose_name='IP', help_text='', null=True)
   
    def __str__(self):
            return self.device.serial.serial_number
        
    class Meta:
        db_table = 'status_info'
        verbose_name = '디바이스 상태 정보'
        verbose_name_plural = '디바이스 상태 리스트'

class Regist(models.Model):
    user = models.ForeignKey(CustomUser,db_column='User_ID', verbose_name='디바이스에 연결된 사용자', help_text='This value must be entered by the owner or by the user specified by the owner.', on_delete=models.CASCADE, related_name='registed_user_id')
    device = models.ForeignKey(Device,db_column='Device_ID', verbose_name='사용자와 연결된 디바이스', help_text='This value must be owner\s device ID', on_delete=models.CASCADE, related_name='registed_device_id')
    ROLE_MASTER= "master"
    ROLE_GUEST= "guest"
    ROLE_OTHER = "other"
    ROLE_CHOICES = (
        (ROLE_MASTER, "Master"),
        (ROLE_GUEST, "Guest"),
        (ROLE_OTHER, "Other"),
    )
    role = models.CharField(
        choices=ROLE_CHOICES, max_length=10,
        db_column='ROLE_CD',
        verbose_name='사용자 권한 코드',
        help_text='This value is entered as a selected one of ROLE_CHOICES',
        default="master"
    )
    created_at = models.DateTimeField(db_column='CRE_DT', verbose_name='생성 날짜', help_text='This value is automatically entered when the table is created.', auto_now_add=True, null=True, blank=True)
    changed_at = models.DateTimeField(db_column='CHG_DT', verbose_name='수정 날짜', help_text='This value is automatically entered when the table is updated.', auto_now=True)
    # deleted_date = models.DateTimeField(null=True, verbose_name='연결해제날짜')
    search_fields = ['role',]
    
    def __str__(self):
            return self.role
        
    class Meta:
        db_table = 'regist_list'
        verbose_name = '사용자 권한 정보'
        verbose_name_plural = '사용자 권한 리스트'
        # unique_together = (('user_id', 'device_id'),)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'device'],
                name = 'unique regist',
                # deferrable = constraints.Deferrable.DEFERRED,
            )
        ]
        
        
class Attachment(models.Model):
    device = models.ForeignKey(Device,db_column='Device_ID', verbose_name='디바이스ID', help_text='This value is automatically entered when the table is created.', on_delete=models.CASCADE)
    master = models.ForeignKey(User,db_column='Master_ID', verbose_name='소유자 ID', help_text='This value is automatically entered when the table is created.', on_delete=models.CASCADE, default='')
    created_at = models.DateTimeField(db_column='CRE_DT', verbose_name='생성 날짜', help_text='This value is automatically entered when the table is created.', auto_now_add=True, null=True)
    
    def __str__(self):
            return '%s의 경로 %s' %(self.device, self.saved_path)
    
    def file_path_for_db(instance, filename): # user와 날짜에 따른 경로 생성을 위한 함수
        pass
    
    # saved_path = models.FileField(db_column='SAVE_PATH', verbose_name='경로', help_text='This value is entered by the file_path_for_db function.', upload_to=file_path_for_db)
    saved_path = models.FileField(db_column='SAVE_PATH', verbose_name='경로', help_text='This value is entered by the file_path_for_db function.', upload_to='')
    
    class Meta:
        db_table = 'attachment_list'
        verbose_name = '영상 파일 정보'
        verbose_name_plural = '영상 파일 리스트'            
        constraints = [
            models.UniqueConstraint(
                fields=['device', 'master'],
                name = 'unique attachments',
                # deferrable = constraints.Deferrable.DEFERRED,
            )
        ]
        
    
class StatusHistory(models.Model):
    user= models.ForeignKey(CustomUser, db_column='UID', verbose_name='소유자', help_text='This value is automatically entered when the table is created.', on_delete=models.CASCADE, default='')
    created_at = models.DateTimeField(db_column='CRE_DT', verbose_name='생성 날짜', help_text='This value is automatically entered when the table is created.', auto_now_add=True, null=True, blank=True)
    device = models.ForeignKey(Device, db_column='Device_ID',verbose_name='디바이스 시리얼 번호', help_text='This value is automatically entered when the table is created.',on_delete=models.CASCADE, default='')
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
        
