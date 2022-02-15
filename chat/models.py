import re
from accounts.models import User
from django.db import models
from django.core.exceptions import ValidationError

class Room(models.Model):
    class RoomType(models.TextChoices):
        PUBLIC = "PUBLIC"
        PRIVATE = "PRIAVATE"
        DM = "DM"
    reg_date = models.DateTimeField('채팅방 생성 날짜', auto_now_add=True)
    name = models.CharField('채팅방 이름', max_length=100, unique=True)
    host = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    part_user = models.ManyToManyField(User, related_name="part_server")
    room_type = models.CharField('채팅방타입', max_length=100, default='basic')
    #status = models.CharField(default="PUBLIC",max_length=20,choices=RoomType.choices)
    def __str__(self):
        return self.name


    


class ChatMessage(models.Model):
    class Message_Type(models.TextChoices):
        ENTER = "ENTER"
        EXIT = "EXIT"
        NORMAL = "NORMAL"
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    writer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    message = models.TextField('메시지 내용')
    timestamp = models.DateTimeField('메시지 전송 시간', auto_now_add=True)
    m_type = models.CharField('메세지타입', max_length=10 , choices= Message_Type.choices, default= Message_Type.NORMAL )

    
class DirectRoom(Room):
    part_user = False
    host = False
    user1 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="user2")