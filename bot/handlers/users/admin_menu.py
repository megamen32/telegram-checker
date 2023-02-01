import csv
import traceback

from aiogram.types import Message, InputFile
from peewee import fn

from loader import dp, bot, config, _
from models.channel import Channel
from services.users import count_users, get_users


@dp.message_handler(i18n_text='Export users 📁', is_admin=True)
@dp.message_handler(commands=['export_users'], is_admin=True)
async def _export_users(message: Message):
    count = count_users()

    file_path = config.DIR / 'users.csv'
    with open(file_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['id', 'name', 'username', 'language', 'created_at'])

        for user in get_users():
            writer.writerow([user.id, user.name, user.username, user.language, user.created_at])

    text_file = InputFile(file_path, filename='users.csv')
    await message.answer_document(text_file, caption=_('Total users: {count}').format(count=count))
@dp.message_handler(i18n_text='Export channels 📁', is_admin=True)
@dp.message_handler(commands=['export_channels'], is_admin=True)
async def _export_channels(message: Message):
    count = Channel.select(fn.COUNT(Channel.id)).scalar()

    file_path = config.DIR / 'channels.csv'
    with open(file_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['name', 'followers_count', 'link'])
        channels=list(Channel.select())

        for channel in channels:
            writer.writerow([channel.name, channel.followers_count, f'https://t.me/{channel.name}'])

    text_file = InputFile(file_path, filename='channels.csv')
    await message.answer_document(text_file, caption=_('Total channels: {count}').format(count=count))

@dp.message_handler(commands=['run'], is_admin=True)
async def _export_users(message: Message):
    from models.channel import  Channel
    command=message.text.split('run ',1)[1]
    try:
        res=eval(command)
    except:
        res=traceback.format_exc(chain=False)
    await message.answer(res)