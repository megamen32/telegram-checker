from aiogram.types import BotCommandScopeDefault, BotCommandScopeChat, BotCommand

from loader import _, bot, i18n
from .default import get_default_commands


def get_admin_commands(lang: str = 'en') -> list[BotCommand]:
    commands = get_default_commands(lang)

    commands.extend([
        BotCommand('/export_users', _('export users to csv', locale=lang)),
        BotCommand('/export_channels', _('export channels to csv', locale=lang)),
    ])

    return commands


async def set_admin_commands(user_id: int, commands_lang: str):
    await bot.set_my_commands(get_admin_commands(commands_lang), scope=BotCommandScopeChat(user_id))
