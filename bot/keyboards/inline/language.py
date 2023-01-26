from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config


def get_language_inline_markup():
    markup = InlineKeyboardMarkup()
    if config('BOT_VARIANT', default=True,cast=bool):
        markup.add(InlineKeyboardButton('🇺🇸 English', callback_data='lang_en_Shaw'))
        markup.add(InlineKeyboardButton('🇷🇺 Русский', callback_data='lang_uk'))
    else:
        markup.add(InlineKeyboardButton('🇺🇸 English', callback_data='lang_en'))
        markup.add(InlineKeyboardButton('🇷🇺 Русский', callback_data='lang_ru'))

    return markup
