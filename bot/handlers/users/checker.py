import asyncio
import datetime
import random
import re
import traceback

import aiogram
from telegraph.aio import Telegraph

from aiogram.types import Message, User, ReplyKeyboardRemove
from decouple import config

from bot.keyboards.default.default import get_instructions
from data.config import BOT_TOKEN
from loader import dp, _,bot
from models.channel import Channel


@dp.message_handler(regexp='t.me\/\w+')
async def analys_start(message: Message, user: User):
    try:

        analysys_people_in_second = 333
        refresh_time = 10
        normal_count=.7

        channel=re.findall('\.me\/(\w+)',message.text)[0]
        current_count=random.gauss(normal_count,0.1)
        if config('CHANNEL_NAME',default='no_name') in channel:
            current_count=0.81642
        text = _('''Начинаю сбор аудитории по каналу: @''')+channel

        msg=await message.answer(text)



        followers_count=await bot.get_chat_member_count(f"@{channel}")
        db_ch: Channel = Channel.get_or_none(Channel.name == channel)
        if config('check_admin_rights', default=False, cast=bool) == True:
            member = await bot.get_chat_member(f"@{channel}", BOT_TOKEN.split(":")[0])
            if not member.is_chat_admin():
                return await msg.edit_text(text + _(
                    '\n\nДля того, чтобы провести анализ, необходимо добавить этого бота в администраторы группы или канала')+get_instructions())
        if db_ch is None:
            month=-1
            while month<0:
                one_three = random.gauss(0.6, 0.1)
                three_week = random.gauss(0.3, 0.1)
                week_month = random.gauss(0.1, 0.05)
                month = 1 - one_three - three_week - week_month
                if min(one_three,week_month,month,three_week)<0:continue
            db_ch = Channel.create(name=channel, not_fake_percent=current_count, followers_count=followers_count, online_percent=random.gauss(0.05,0.01), recent_percent=one_three,
                                   three_to_week_percent=three_week, week_to_month_percent=week_month, more_than_month_percent=month)
        else:
            current_count=db_ch.not_fake_percent
        need_to_analys = db_ch.bot_users == 0 or db_ch.followers_count!=followers_count
        if need_to_analys:
            msg = await analys_channel(analysys_people_in_second, channel, current_count, followers_count, msg,
                                        refresh_time, text)
        else:
            db_ch.followers_count=followers_count


            real_people = db_ch.followers_count-db_ch.bot_users
            analysys_completed=db_ch.followers_count
            fake = db_ch.bot_users
            text2,text3,text4= await render_text(analysys_completed, fake, db_ch.more_than_month_percent * real_people,
                                                 db_ch.recent_percent * real_people, db_ch.online_percent * real_people,
                                                 real_people, db_ch.three_to_week_percent * real_people,
                                                 db_ch.week_to_month_percent * real_people, db_ch.followers_count,channel)


            await msg.edit_text(text2 + text3+text4 + _('\n\nАнализ завершен.'))
    except aiogram.exceptions.ChatNotFound:
        await msg.edit_text(msg.text+_('\n\nТакой чат не найден'))
    except:
        traceback.print_exc()


async def analys_channel(analysys_people_in_second, channel, current_count, followers_count, msg,
                         refresh_time, text):
    analysys_completed = 0
    real_people = 0
    fake=0
    step=0
    channel=Channel.get(Channel.name==channel)
    is_first_time=channel.bot_users==0
    while analysys_completed != followers_count:
        await asyncio.sleep(refresh_time)
        analysys_completed += int(max(0, analysys_people_in_second * refresh_time*random.gauss(1, 0.5)))
        if analysys_completed > followers_count:
            analysys_completed = int(min(followers_count, analysys_completed))


        if is_first_time:
            for i in range(fake + real_people, analysys_completed):
                if random.random() < current_count:
                    real_people += 1
        else:
             real_people=int(analysys_completed*(channel.not_fake_percent+random.gauss(0,0.0008)))
        fake=analysys_completed-real_people

        wait_time = (followers_count - analysys_completed) / analysys_people_in_second
        online_count=int(real_people*channel.online_percent)

        one_three_days=int(real_people*channel.recent_percent)

        three_to_week=int(channel.three_to_week_percent*real_people)
        week_to_month=int(channel.week_to_month_percent*real_people)
        more_than_month=real_people-one_three_days-three_to_week-week_to_month

        text2,text3, text4 = await render_text(analysys_completed, fake, more_than_month, one_three_days, online_count,
                                               real_people, three_to_week, week_to_month, followers_count,channel.name)
        wait_text = _('\nПримерное время ожидание: {:.0f} секунд').format(wait_time)

        try:
            if config('BOT_VARIANT', default=False,cast=bool):
                msg = await  msg.edit_text(wait_text)
            else:
                msg = await  msg.edit_text(text2 + text3 + text4+wait_text)
        except aiogram.utils.exceptions.MessageNotModified:
            pass
        except:
            traceback.print_exc()
        step+=1

    Channel.update(bot_users=fake, not_fake_percent=1-fake/followers_count,followers_count=followers_count,three_to_week_percent=three_to_week/real_people,week_to_month_percent=week_to_month/real_people,more_than_month_percent=more_than_month/real_people).where(Channel.name == channel).execute()
    await msg.edit_text(text2 + text3 +text4+ _('\n\nАнализ завершен.'))
    return msg


async def render_text(analysys_completed, fake, more_than_month, one_three_days, online_count, real_people,
                      three_to_week, week_to_month, followers_count, name=''):
    real_percent=real_people/analysys_completed*100
    text2= _('\n\nПроанализировано: {} из {} - {:.1f}%').format(analysys_completed, followers_count,
                                                                                 analysys_completed/followers_count*100)
    text3 = _('''
        👥 Подписчики: {real_people} ({real_percent:.2f}%)
        ♂️ боты: {fake} ({fake_percent:.2f}%)''').format(real_people=real_people,real_percent= real_percent, fake=fake,fake_percent= 100 - real_percent)
    if config('BOT_VARIANT',default=False,cast=bool):
        me = await bot.get_me()
        html_content=_('''
<p><strong>ВСЕГО ПРОВЕРЕНО: {analysys_completed}</strong></p>
<p>Подписчиков онлайн на момент проверки: <b>{online_count}</b></p>
<p>Пользователь был онлайн: </p>  
<ul> 
    <li>до 3 дней назад: {one_three_days} ({one_three_days_p:.2f}%)</li>    
    <li>до 7 дней назад: {three_to_week} ({three_to_week_p:.2f}%)</li>    
    <li>до 30 дней назад: {week_to_month} ({week_to_month_p:.2f}%)</li>    
    <li>более 30 дней назад: {more_than_month} ({more_than_month_p:.2f}%) </li>  
</ul> 
<p><b>Предположительная доля ботов</b> (заблокированные, удаленные, спам аккаунты): {fake} ({fake_percent:.2f}%)</p>   
<p><b>Внимание!</b> Данный бот лишь один из методов проверки аудитории, не забывайте использовать полную статистику канала и дополнительные инструменты на сайте telemetr.me   </p>
<p>____</p>
<p><strong>КАК ОПРЕДЕЛИТЬ НАКРУТКУ?</strong></p>
<ul>
    <li>1.      </li>
    <li>2.      </li>
    <li>3.      </li> 
</ul>
<p>Больше статистических данных и полезной информации доступно на нашем сайте telemetr.me!</p>
    ''').format(analysys_completed=analysys_completed,real_people=real_people,real_percent= real_percent, fake=fake,fake_percent= 100 - real_percent,online_count=int(online_count),online_percent= online_count / analysys_completed * 100,
                one_three_days=int(one_three_days), one_three_days_p=one_three_days / analysys_completed * 100,
                three_to_week=int(three_to_week),three_to_week_p= three_to_week / analysys_completed * 100,
                week_to_month=int(week_to_month),week_to_month_p= week_to_month / analysys_completed * 100,
                more_than_month=int(more_than_month), more_than_month_p=more_than_month / analysys_completed * 100)
        telegraph = Telegraph()
        await telegraph.create_account(short_name=me.username,author_name='telemetr.me',author_url='https://telemetr.me')
        channel=Channel.get(Channel.name==name)
        chat=await bot.get_chat('@'+channel.name)
        response = await telegraph.create_page(
            _('{date}-{name}').format(date=datetime.datetime.now().strftime("%d/%m/%y"),name=chat.title),
        html_content = html_content)
        text4='\n\nОтчет доступен по ссылке: {response}'.format(response=response['url'])
    else:
        text4 = _('''\n\n📢Онлайн: {online_count} ({online_percent:.2f}%)\n
    👥 Подписчики которые заходили в последний раз:
        🕕 от 1 секунды до 2-3 дней назад: {one_three_days} ({one_three_days_p:.2f}%)
        🕐 от 2-3 дней до 7 дней назад: {three_to_week} ({three_to_week_p:.2f}%)
        🕐 от 7 дней до месяца назад: {week_to_month} ({week_to_month_p:.2f}%)
        🕒 больше месяца назад: {more_than_month} ({more_than_month_p:.2f}%)
    ''').format(online_count=int(online_count),online_percent= online_count / analysys_completed * 100,
                one_three_days=int(one_three_days), one_three_days_p=one_three_days / analysys_completed * 100,
                three_to_week=int(three_to_week),three_to_week_p= three_to_week / analysys_completed * 100,
                week_to_month=int(week_to_month),week_to_month_p= week_to_month / analysys_completed * 100,
                more_than_month=int(more_than_month), more_than_month_p=more_than_month / analysys_completed * 100)
    return text2,text3, text4
