import asyncio
import random
import re
import traceback

import aiogram
from aiogram.types import Message, User, ReplyKeyboardRemove

from loader import dp, _,bot
from models.channel import Channel


@dp.message_handler(regexp='t.me\/\w+')
async def analys_start(message: Message, user: User):
    try:

        analysys_peapole_in_second = 333
        refresh_time = 10
        normal_count=.8

        current_count=random.gauss(normal_count,0.1)
        channel=re.findall('\.me\/(\w+)',message.text)[0]
        text = _('''Начинаю сбор аудитории по каналу: @''')+channel

        msg=await message.answer(text)



        followers_count=await bot.get_chat_member_count(f"@{channel}")
        db_ch: Channel = Channel.get_or_none(Channel.name == channel)
        if db_ch is None:
            db_ch = Channel.create(name=channel, not_fake_percent=current_count,followers_count=followers_count)
        else:
            current_count=db_ch.not_fake_percent
        need_to_analys = db_ch.bot_users == 0 or db_ch.followers_count!=followers_count
        if need_to_analys:
            msg = await analys_channel(analysys_peapole_in_second, channel, current_count, followers_count, msg,
                                        refresh_time, text)
        else:
            db_ch.followers_count=followers_count
            text2 = text + _('\n\nПроанализированно: {} из {} - {:.1f}%').format(followers_count, followers_count,
                                                                                 followers_count / followers_count * 100)

            real_peapole = db_ch.followers_count-db_ch.bot_users
            analysys_completed=db_ch.followers_count
            fake = db_ch.bot_users
            real_percent = real_peapole / analysys_completed * 100
            text3 = _('''
                💚 Подписчики: {} ({:.2f}%)
                ♂️ боты: {} ({:.2f}%)''').format(real_peapole, real_percent, fake, 100 - real_percent)
            await msg.edit_text(text2 + text3 + _('\n\nАнализ завершен.'))
    except aiogram.exceptions.ChatNotFound:
        await msg.edit_text(msg.text+_('\n\nChat with that name not found'))
    except:
        traceback.print_exc()


async def analys_channel(analysys_peapole_in_second, channel, current_count, followers_count, msg,
                         refresh_time, text):
    analysys_completed = 0
    real_peapole = 0
    fake=0
    prev_percent=0
    step=0
    channel=Channel.get(Channel.name==channel)
    is_first_time=channel.bot_users==0
    while analysys_completed != followers_count:

        analysys_completed += int(max(0, random.gauss(analysys_peapole_in_second * refresh_time, 1000)))
        if analysys_completed > followers_count:
            analysys_completed = int(min(followers_count, analysys_completed))

        text2 = text + _('\n\nПроанализированно: {} из {} - {:.1f}%').format(analysys_completed, followers_count,                                                                     analysys_completed / followers_count * 100)

        if is_first_time:
            for i in range(fake + real_peapole, analysys_completed):
                if random.random() < current_count:
                    real_peapole += 1
        else:
             real_peapole=int(analysys_completed*(channel.not_fake_percent+random.gauss(0,0.008)))
        fake=analysys_completed-real_peapole

        if analysys_completed > 0:
            real_percent = real_peapole / analysys_completed * 100
        else:
            real_percent = 100.00
        wait_time = (followers_count - analysys_completed) / analysys_peapole_in_second
        text3 = _('''
        💚 Подписчики: {} ({:.2f}%)
        ♂️ боты: {} ({:.2f}%)''').format(real_peapole, real_percent, fake, 100 - real_percent)
        text4 = _('\nПримерное время ожидание: {:.0f} секунд').format(wait_time)

        try:
            msg = await  msg.edit_text(text2 + text3 + text4)
        except aiogram.utils.exceptions.MessageNotModified:
            pass
        except:
            traceback.print_exc()
        step+=1
        await asyncio.sleep(refresh_time)
    Channel.update(bot_users=fake, not_fake_percent=1-fake/followers_count,followers_count=followers_count).where(Channel.name == channel).execute()
    await msg.edit_text(text2 + text3 + _('\n\nАнализ завершен.'))
    return msg
