import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.utils.i18n import FSMI18nMiddleware, I18n

from commands.main_commands import main_commands
from handler.main_keyboard import main_keyboard
from routers.send_to_admin import send_to_admin
from routers.worker import worker_router

TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()

async def on_startup(bot: Bot) -> None:
    command_list = [
        BotCommand(command='start', description='botni ishga tushrish'),
        BotCommand(command='help', description="ma'lumot olishg")
    ]
    await bot.set_my_commands(command_list)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    i18n = I18n(path="locales", default_locale="en", domain="messages")
    dp.update.outer_middleware(FSMI18nMiddleware(i18n))
    dp.startup.register(on_startup)
    dp.include_routers(main_commands, main_keyboard, send_to_admin, worker_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

