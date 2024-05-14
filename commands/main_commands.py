from os import getenv

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_commands = Router()
TOKEN = getenv('BOT_TOKEN')


def make_main_menu1(**kwargs):
    rkb = ReplyKeyboardBuilder()
    rkb.add(
            KeyboardButton(text=_("Sherik kerak", **kwargs)),
            KeyboardButton(text=_("Ish joyi kerak", **kwargs)),
            KeyboardButton(text=_("Xodim kerak", **kwargs)),
            KeyboardButton(text=_("Ustoz kerak", **kwargs)),
            KeyboardButton(text=_("Shogird kerak", **kwargs)),
            KeyboardButton(text=_("Tilni o'zgartirish", **kwargs))
            )
    rkb.adjust(2, repeat=True)
    return rkb.as_markup(resize_keyboard=True)


@main_commands.message(CommandStart())
async def start(message: Message):
    await message.answer(_('''<b>Assalom alaykum {name}\nUstoz Shogird kanalining rasmiy botiga xush kelibsiz!</b>\n
/help yordam buyrugi orqali nimalarga qodir ekanligimni bilib oling!'''.format(name=message.from_user.full_name),
                           ), reply_markup=make_main_menu1())


@main_commands.message(Command(commands=['help']))
async def help(message: Message):
    text = _('''
P22 group faoli tomonidan tuzilgan Ustoz-Shogird kanali.

Bu yerda Programmalash bo`yicha
  #Ustoz,
  #Shogird,
  #oquvKursi,
  #Sherik,
  #Xodim va
  #IshJoyi
 topishingiz mumkin.

E'lon berish: @usta_shogirt1_bot

Admin @shahriyor447''')
    await message.answer(text)
