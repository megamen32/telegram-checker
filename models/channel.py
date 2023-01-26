from datetime import datetime

from peewee import BigIntegerField, CharField, BooleanField, DateTimeField, IntegerField, FloatField

from .base import BaseModel


class Channel(BaseModel):
    name = CharField(default=None,primary_key=True)
    followers_count=IntegerField(default=0)
    not_fake_percent=FloatField(default=0.8)
    bot_users=IntegerField(default=0)
    online_percent=FloatField(default=0.05)
    recent_percent=FloatField(default=0.6)
    three_to_week_percent=FloatField(default=0.2)
    week_to_month_percent=FloatField(default=0.1)
    more_than_month_percent=FloatField(default=0.1)

    def __repr__(self) -> str:
        return f'<Channel {self.name}>'

    class Meta:
        table_name = 'channels'
