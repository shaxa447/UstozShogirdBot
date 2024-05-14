from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _

def yes_no():
    rkb = ReplyKeyboardBuilder([[KeyboardButton(text=_("Ha"))],
                                [KeyboardButton(text=_("Yo'q"))]])
    rkb.adjust(2)
    return rkb.as_markup(resize_keyboard=True)
