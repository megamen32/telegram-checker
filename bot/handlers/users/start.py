from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp
from aiogram.types import Message

from bot.commands import get_admin_commands, get_default_commands
from bot.commands import set_admin_commands
from bot.keyboards.inline import get_language_inline_markup
from loader import dp, _
from models import User


@dp.message_handler(CommandStart())
async def _start(message: Message, user: User):
    if user.is_admin:
        await set_admin_commands(user.id, user.language)

    text = _('''Выберите язык / Choose language:''')

    await message.answer(text, reply_markup=get_language_inline_markup())




@dp.message_handler(i18n_text='Help 🆘')
@dp.message_handler(CommandHelp())
async def _help(message: Message, user: User):
    commands = get_admin_commands(user.language) if user.is_admin else get_default_commands(user.language)

    text = _('Help 🆘') +_('\n\nПришли ссылку на канал, чтобы провезти анализ. Например: t.me/TGStat\n\n')
    for command in commands:
        text += f'{command.command} - {command.description}\n'

    await message.answer(text)
