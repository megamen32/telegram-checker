from aiogram.types import Message

from bot.keyboards.default import get_default_markup
from loader import dp, _
from models import User


@dp.message_handler(state='*')
async def _default_menu(message: Message, user: User):
    await message.answer(_('Choose an action from the menu 👇'), reply_markup=get_default_markup(user))

def get_instructions():
    text = _('\n\n Инструкция: https://telegra.ph/Instrukciya-ispolzovaniya-TGStat-Bot-Checker-01-26')
    return text