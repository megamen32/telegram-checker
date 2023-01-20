from aiogram.dispatcher.filters.builtin import Regexp
from aiogram.types import CallbackQuery, Message

from bot.commands import set_admin_commands, set_user_commands
from bot.keyboards.default import get_default_markup
from bot.keyboards.inline import get_language_inline_markup
from loader import dp, _, i18n
from models import User
from services.users import edit_user_language


@dp.callback_query_handler(Regexp('^lang_(\w\w)$'))
async def _change_language(callback_query: CallbackQuery, regexp: Regexp, user: User):
    language = regexp.group(1)

    edit_user_language(callback_query.from_user.id, language)
    i18n.set_user_locale(language)

    await set_admin_commands(user.id, language) if user.is_admin else await set_user_commands(user.id, language)
    dicts={'ru':'Русский','en':'English','uk':'Українська'}
    await callback_query.message.answer(_(f'Выбран язык: {dicts[language]}\n'))
    await get_welcome_screen(callback_query.message,user)
async def get_welcome_screen(message: Message,user:User):

    text = _('''Для получения статистики канала или чата отправьте боту ссылку на него.''')

    await message.answer(text)


@dp.message_handler(i18n_text='Settings 🛠')
@dp.message_handler(commands=['lang', 'settings'])
async def _settings(message: Message):
    text = _('Choose your language')

    await message.answer(text, reply_markup=get_language_inline_markup())
