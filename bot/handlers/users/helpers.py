from aiogram.types import Message

from bot.keyboards.default import get_default_markup
from bot.keyboards.default.default import get_instructions
from loader import dp, _
from models import User


@dp.message_handler(state='*')
async def _default_menu(message: Message, user: User):
    await message.answer(get_instructions())

