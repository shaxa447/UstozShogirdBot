from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from config import ADMIN_LIST

send_to_admin = Router()

def make_main_menu(**kwargs):
    rkb = ReplyKeyboardBuilder([[KeyboardButton(text=_("Sherik kerak", **kwargs))],
                                [KeyboardButton(text=_("Ish joyi kerak", **kwargs))],
                                [KeyboardButton(text=_("Xodim kerak", **kwargs))],
                                [KeyboardButton(text=_("Ustoz kerak", **kwargs))],
                                [KeyboardButton(text=_("Shogird kerak", **kwargs))],
                                [KeyboardButton(text=_("Tilni o'zgartirish", **kwargs))]])
    rkb.adjust(2, repeat=True)
    return rkb.as_markup(resize_keyboard=True)
@send_to_admin.message(F.text == __('Ha'))
async def hello(message: Message, bot: Bot, state: FSMContext):
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text=_('✅Qabul qilish'), callback_data=f'admin_confirm_{message.from_user.id}'),
            InlineKeyboardButton(text=_('❌Bekor qilish'), callback_data=f'admin_cancel_{message.from_user.id}'))
    ikb.adjust(2)
    data = await state.get_data()
    for admin in ADMIN_LIST:
        await bot.send_message(admin, data['text'], reply_markup=ikb.as_markup())
    await message.answer(
        _("📪 So`rovingiz tekshirish uchun adminga jo`natildi!\n\nE'lon 24-48 soat ichida kanalda chiqariladi."))



@send_to_admin.callback_query(F.data.startswith('admin_'))
async def admin_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    bool = callback.data.split('_')[1]
    user_id = callback.data.split('_')[-1]
    data = await state.get_data()
    msg = data.get('text')
    await state.clear()
    if bool == 'confirm':
        await callback.message.delete()
        await bot.send_message(chat_id=str(-1002104432737), text=msg)
        await bot.send_message(chat_id=user_id, text=_('🎉 Arizangiz admin tominidan qabul qilindi'), reply_markup=make_main_menu())
    else:
        await callback.message.delete()
        await bot.send_message(chat_id=user_id, text=_('❌ Arizangiz admin tominidan qabul qilinmadi'), reply_markup=make_main_menu())




@send_to_admin.message(F.text == __("Yo'q"))
async def abs_send_to_admin(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(_('Bekor qilindi.\nTanlang'), reply_markup=make_main_menu())