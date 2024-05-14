from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from handler.yes_no import yes_no
from routers.send_to_admin import make_main_menu
from state import Form

main_keyboard = Router()

d = {
    'Ustoz': 'Shogird',
    'Shogird': 'Ustoz',
    'Ish': 'Xodim',
    'Sherik': 'Sherik'
}


@main_keyboard.message(F.text == __("Tilni o'zgartirish"))
async def change_language(message: Message):
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text=_("🇺🇿o'zbek"), callback_data='lang_uz'),
            InlineKeyboardButton(text=_("🇬🇧ingliz"), callback_data='lang_en'))
    ikb.adjust(2)
    await message.answer(_('Tilni tanlang'), reply_markup=ikb.as_markup())


@main_keyboard.callback_query(F.data.startswith('lang_'))
async def languages(callback: CallbackQuery, state: FSMContext) -> None:
    lang_code = callback.data.split('lang_')[-1]
    await state.update_data(locale=lang_code)
    if lang_code == 'uz':
        lang = _("O'zbek", locale=lang_code)
    else:
        lang = _('Ingliz', locale=lang_code)
    await callback.answer(_('{lang} tili tanlandi', locale=lang_code).format(lang=lang))

    rkb = make_main_menu(locale=lang_code)
    msg = _('Assalomu aleykum! Tanlang.', locale=lang_code)
    await callback.message.answer(text=msg, reply_markup=rkb)


@main_keyboard.message(F.text.startswith(('Partner', 'Workplace', 'Teacher', 'Apprentice')))
async def partner(message: Message, state: FSMContext):
    rkb = ReplyKeyboardRemove()
    await state.update_data(key=message.text)
    status = message.text.split()[0]
    answer_status = d.get(status)
    await state.update_data(answer_status=answer_status)
    text = '''
to find {space} filing an application

Now you will be asked some questions. 
Answer each one. 
At the end, if everything is correct, press the YES button and your applicationIt will send to admin.
'''.format(space=message.text[: -6])
    await message.answer(text, reply_markup=rkb)
    await state.set_state(Form.name)
    await message.answer(_('Ism, familiyangizni kiriting?'))


@main_keyboard.message(F.text.startswith(("Ish joyi", 'Ustoz', 'Shogird', 'Sherik')))
async def show_joyi(message: Message, state: FSMContext):
    rkb = ReplyKeyboardRemove()
    await state.update_data(key=message.text)
    status = message.text.split()[0]
    answer_status = d.get(status)
    await state.update_data(answer_status=answer_status)
    text = _('''
{space} topish uchun ariza berish

Hozir sizga birnecha savollar beriladi. 
Har biriga javob bering. 
Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.
    '''.format(space=message.text[: -6]))
    await message.answer(text, reply_markup=rkb)
    await state.set_state(Form.name)
    await message.answer(_('Ism, familiyangizni kiriting?'))


@main_keyboard.message(Form.name)
async def show_form(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(name=message.text)
    if data.get('key') != _('Sherik kerak'):
        await state.set_state(Form.age)
        await message.answer(_('🕑 Yosh: \n\nYoshingizni kiriting?\nMasalan, 19'))
    else:
        await state.set_state(Form.technology)
        await message.answer(
            _('📚 Texnologiya:\n\nTalab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating.\nMasalan, Java, C++, C#'))


@main_keyboard.message(Form.age)
async def show_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Form.technology)
    await message.answer(
        _('📚 Texnologiya:\n\nTalab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating.\nMasalan, Java, C++, C#'))


@main_keyboard.message(Form.technology)
async def show_technology(message: Message, state: FSMContext):
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text=_('Telefon raqam'), request_contact=True))
    await state.update_data(technology=message.text)
    await state.set_state(Form.phone_number)
    await message.answer(
        _('📞 Aloqa: \n\nBog`lanish uchun button orqali yuboring yoki raqamingizni kiriting?\nMasalan, 998 90 123 45 67'),
        reply_markup=rkb.as_markup(resize_keyboard=True))


@main_keyboard.message(Form.phone_number)
async def show_technology(message: Message, state: FSMContext):
    rkb = ReplyKeyboardRemove()
    if message.content_type == 'contact':
        phone = message.contact.phone_number
    else:
        phone = message.text
    await state.update_data(phone_number=phone)
    await state.set_state(Form.place)
    await message.answer(
        _('🌐 Hudud: \n\nQaysi hududdansiz?\nViloyat nomi, Toshkent shahar yoki Respublikani kiriting.'),
        reply_markup=rkb)


@main_keyboard.message(Form.place)
async def show_technology(message: Message, state: FSMContext):
    await state.update_data(place=message.text)
    await state.set_state(Form.salary)
    await message.answer(_('💰 Narxi:\n\nTolov qilasizmi yoki Tekinmi?\nKerak bo`lsa, Summani kiriting?'))


@main_keyboard.message(Form.salary)
async def show_technology(message: Message, state: FSMContext):
    await state.update_data(salary=message.text)
    await state.set_state(Form.job)
    await message.answer(_('👨🏻‍💻 Kasbi: \n\nIshlaysizmi yoki o`qiysizmi?\nMasalan, Talaba'))


@main_keyboard.message(Form.job)
async def show_technology(message: Message, state: FSMContext):
    await state.update_data(job=message.text)
    await state.set_state(Form.time_connect)
    await message.answer(_('🕰 Murojaat qilish vaqti:\n\nQaysi vaqtda murojaat qilish mumkin?\nMasalan, 9:00 - 18:00'))


@main_keyboard.message(Form.time_connect)
async def show_technology(message: Message, state: FSMContext):
    await state.update_data(time_connect=message.text)
    await state.set_state(Form.aim)
    await message.answer(_('🔎 Maqsad: \n\nMaqsadingizni qisqacha yozib bering.'))


@main_keyboard.message(Form.aim)
async def show_aim(message: Message, state: FSMContext):
    await state.update_data(aim=message.text)
    if message.from_user.username:
        user = '@' + message.from_user.username
    else:
        user = message.from_user.full_name
    data = await state.get_data()
    if data.get('answer_status') == _('Shogird') or data.get('answer_status') == _('Ustoz'):
        hashtag = _('shogird')
    elif data.get('answer_status') == _('Sherik'):
        hashtag = _('sherik')
    else:
        hashtag = _('ishjoyi')
    await state.clear()
    if data.get('age'):
        text_adition = _('\n🌐 Yosh: {age}').format(age=data.get('age'))
    else:
        text_adition = ''
    text = _('''
<b>{key}</b>

🎓{answer_status}: {name}{text_adition}
📚 Texnologiya: {technology}
🇺🇿 Telegram: {user}
📞 Aloqa: +{phone_number}
🌐 Hudud: {place}
💰 Narxi: {salary}
👨🏻‍💻 Kasbi: {job}
🕰 Murojaat qilish vaqti: {time_connect}
🔎 Maqsad: {aim}    
    
#{hashtag}
    ''').format(key=data['key'], answer_status=data['answer_status'], name=data['name'],
                age=data.get('age', {}), technology=data['technology'], user=user, hashtag=hashtag,
                phone_number=data['phone_number'], place=data['place'], salary=data['salary'],
                job=data['job'], time_connect=data['time_connect'], aim=data['aim'], text_adition=text_adition)
    await state.update_data(text=text)
    await message.answer(text, reply_markup=yes_no())
    await message.answer(_("Barcha ma'lumotlar to'g'rimi?"))
