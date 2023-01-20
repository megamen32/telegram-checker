import asyncio
import random
import re
import traceback

import aiogram
from aiogram.types import Message, User, ReplyKeyboardRemove

from loader import dp, _,bot


@dp.message_handler(regexp='t.me\/\w+')
async def analys_start(message: Message, user: User):
    try:

        analysys_peapole_in_second = 333
        refresh_time = 10
        normal_count=.8

        current_count=random.gauss(normal_count,0.1)
        channel=re.findall('t.me\/(\w+)',message.text)[0]
        text = _('''Начинаю сбор аудиторию по каналу: @''')+channel

        msg=await message.answer(text)
        followers_count=await bot.get_chat_member_count(f"@{channel}")
        analysys_completed=0
        prev_real_peapole=0
        prev_fake_peapole=0
        while analysys_completed<=followers_count:
            text2=text+_('\n\nПроанализированно: {} из {} - {:.1f}%').format(analysys_completed,followers_count,analysys_completed/followers_count*100)

            real_peapole=0
            for i in range(analysys_completed):
                if random.random()<current_count:
                    real_peapole+=1
            if analysys_completed-real_peapole<prev_fake_peapole:
                real_peapole=analysys_completed-prev_fake_peapole

            prev_real_peapole=real_peapole

            fake=analysys_completed-real_peapole
            prev_fake_peapole = fake
            if analysys_completed>0:
                real_percent = real_peapole / analysys_completed * 100
            else:
                real_percent=100.00
            wait_time=(followers_count-analysys_completed)/analysys_peapole_in_second
            text3=_('''
    💚 Подписчики: {} ({:.0f}%)
    ♂️ боты: {} ({:.0f}%)
    Примерное время ожидание: {:.0f} секунд''').format(real_peapole, real_percent, fake,100-real_percent,wait_time)


            if analysys_completed>0:
                await asyncio.sleep(refresh_time)
            try:
                msg = await  msg.edit_text(text2 + text3)
            except aiogram.utils.exceptions.MessageNotModified:pass
            except:
                traceback.print_exc()

            analysys_completed+=int(random.gauss(analysys_peapole_in_second*refresh_time,3000))
            if analysys_completed==followers_count:
                break
            if analysys_completed>followers_count:
                analysys_completed=int(min(followers_count,analysys_completed))

        await msg.edit_text(msg.text+'\n\nАнализ завершен.')
    except:
        traceback.print_exc()
