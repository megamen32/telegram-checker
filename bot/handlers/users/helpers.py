from aiogram.types import Message
from decouple import config

from bot.keyboards.default import get_default_markup
from bot.keyboards.default.default import get_instructions,get_example
from loader import dp, _
from models import User


@dp.message_handler(state='*')
async def _default_menu(message: Message, user: User):
    if config('BOT_VARIANT',default=False,cast=bool):
        await message.answer(_('Choose an action from the menu 👇'), reply_markup=get_default_markup(user))
    else:
        await message.answer(get_example()+ get_instructions())

