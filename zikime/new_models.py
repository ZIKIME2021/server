from django.db import models
from django.contrib.auth.models import User
from django.db.models import constraints

class CustomUser(User):
    
    def __str__(self):
            return self.username
    
    class Meta:
        proxy = True
        db_table = 'user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자 리스트'
        ordering = ('username',)


