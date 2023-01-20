from datetime import datetime

from peewee import BigIntegerField, CharField, BooleanField, DateTimeField, IntegerField, FloatField

from .base import BaseModel


class Channel(BaseModel):
    name = CharField(default=None,primary_key=True)
    followers_count=IntegerField(default=0)
    not_fake_percent=FloatField(default=0.8)
    bot_users=IntegerField(default=0)

    def __repr__(self) -> str:
        return f'<Channel {self.name}>'

    class Meta:
        table_name = 'channels'
