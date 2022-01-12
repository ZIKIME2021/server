# Generated by Django 3.2.9 on 2022-01-12 15:18

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(db_column='UID', max_length=100, unique=True, verbose_name='username')),
                ('password', models.CharField(db_column='PW', max_length=200, verbose_name='password')),
                ('email', models.EmailField(db_column='EMAIL', max_length=50, verbose_name='email')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '사용자',
                'verbose_name_plural': '사용자 리스트',
                'db_table': 'user',
                'ordering': ('username',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(db_column='Serial_ID', help_text='This value is automatically entered by reference.', max_length=100, verbose_name='시리얼 번호')),
                ('nickname', models.CharField(db_column='Nickname', default='닉네임 없음', max_length=30, verbose_name='기기 닉네임')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='CRE_DT', help_text='This value is automatically entered when the table is created.', null=True, verbose_name='생성 날짜')),
                ('master', models.ForeignKey(db_column='Master', default='', on_delete=django.db.models.deletion.CASCADE, related_name='master', to=settings.AUTH_USER_MODEL, verbose_name='마스터')),
            ],
            options={
                'verbose_name': '디바이스',
                'verbose_name_plural': '디바이스 리스트',
                'db_table': 'Device',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='CRE_DT', help_text='This value is automatically entered when the table is created.', null=True, verbose_name='생성 날짜')),
                ('mode', models.CharField(db_column='Mode_ST', default='N', help_text='If the state is normal N is if the the state is emergency F is automatically entered.', max_length=1, verbose_name='디바이스 모드')),
                ('latitude', models.FloatField(db_column='Latitude_ST', default=0.0, help_text='This value is automatically entered by receiving the status of the connected device', verbose_name='위도')),
                ('longitude', models.FloatField(db_column='longitude_ST', default=0.0, help_text='This value is automatically entered by receiving the status of the connected device', verbose_name='경도')),
                ('altitude', models.FloatField(db_column='altitude_ST', default=0.0, help_text='This value is automatically entered by receiving the status of the connected device', verbose_name='고도')),
                ('ONF', models.BooleanField(db_column='ONF_ST', default=True, help_text='This vaule is automatically entered by receiving the status of the connected device', verbose_name='디바이스 On/Off')),
                ('IP', models.GenericIPAddressField(db_column='IP_INFO', null=True, verbose_name='IP')),
                ('device', models.OneToOneField(db_column='Device_ID', default='', help_text='This value is automatically entered when the table is created.', on_delete=django.db.models.deletion.CASCADE, to='zikime.device', verbose_name='디바이스 시리얼 번호')),
                ('user', models.OneToOneField(db_column='UID', help_text='This value is automatically entered when the table is created.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='소유자')),
            ],
            options={
                'verbose_name': '이전 기록',
                'verbose_name_plural': '이전 기록 리스트',
                'db_table': 'history_info',
            },
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.ForeignKey(db_column='Device', on_delete=django.db.models.deletion.CASCADE, related_name='device', to='zikime.device', verbose_name='디바이스 id')),
                ('user', models.ForeignKey(db_column='User', on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='유저 id')),
            ],
            options={
                'verbose_name': '게스트',
                'verbose_name_plural': '게스트 리스트',
                'db_table': 'Guest',
            },
        ),
        migrations.AddConstraint(
            model_name='history',
            constraint=models.UniqueConstraint(fields=('created_at', 'user', 'device'), name='unique history'),
        ),
        migrations.AddConstraint(
            model_name='device',
            constraint=models.UniqueConstraint(fields=('serial',), name='unique device'),
        ),
    ]
