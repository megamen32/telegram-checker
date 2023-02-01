from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from loader import _


def get_default_markup(user):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    markup.add(_('Help 🆘'), _('Settings 🛠'))

    if user.is_admin:
        markup.add(_('Export users 📁'))
        markup.add(_('Export channels 📁'))

    if len(markup.keyboard) < 1:
        return ReplyKeyboardRemove()

    return markup
def get_instructions():
    text = _('\n\n Инструкция: https://telegra.ph/Instrukciya-ispolzovaniya-TGStat-Bot-Checker-01-26')
    return text
def get_example():
    return _('\nПришли ссылку на канал, чтобы провести анализ. Например: t.me/TGStat')
