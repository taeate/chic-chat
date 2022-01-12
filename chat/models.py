from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Room(models.Model):
    reg_date = models.DateTimeField('채팅방 생성 날짜', auto_now_add=True)
    name = models.CharField('채팅방 이름', max_length=100, unique=True)
    host = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Massage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    message = models.TextField('메시지 내용')
    timestamp = models.DateTimeField('메시지 전송 시간', auto_now_add=True)
