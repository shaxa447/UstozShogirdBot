from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from handler.yes_no import yes_no
from state import Form

worker_router = Router()


@worker_router.message(F.text == __('Xodim kerak'))
async def xodim(message: Message, state: FSMContext):
    rkb = ReplyKeyboardRemove()
    space = message.text.split()[0]
    await state.update_data(key=message.text)
    text = _('''
{space} topish uchun ariza berish

Hozir sizga birnecha savollar beriladi. 
Har biriga javob bering. 
Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.
'''.format(space=space))
    await message.answer(text, reply_markup=rkb)
    await state.set_state(Form.office)
    await message.answer(_('🎓 Idora nomi?'))


@worker_router.message(Form.office)
async def office(message: Message, state: FSMContext):
    await state.update_data(office=message.text)
    text = _('''
📚 Texnologiya:

Talab qilinadigan texnologiyalarni kiriting?
Texnologiya nomlarini vergul bilan ajrating. Masalan, 

Java, C++, C#    
''')
    await state.set_state(Form.technology_)
    await message.answer(text)


@worker_router.message(Form.technology_)
async def sho_technology(message: Message, state: FSMContext):
    rkb = ReplyKeyboardBuilder()
    rkb.row(KeyboardButton(text=_("Telefon raqam"), request_contact=True))
    await state.update_data(technology_=message.text)
    await state.set_state(Form.call)
    text = _('''
📞 Aloqa: 

Bog`lanish uchun buttonni bosing yoki raqamingizni kiriting?
Masalan, 998 90 123 45 67    
''')
    await message.answer(text, reply_markup=rkb.as_markup(resize_keyboard=True))


@worker_router.message(Form.call)
async def technology(message: Message, state: FSMContext):
    rkm = ReplyKeyboardRemove()
    if message.content_type == 'contact':
        call = message.contact.phone_number
    else:
        call = message.text
    await state.update_data(call=call)
    await state.set_state(Form.place_)
    text = _('''
🌐 Hudud: 

Qaysi hududdansiz?
Viloyat nomi, Toshkent shahar yoki Respublikani kiriting.  
''')
    await message.answer(text, reply_markup=rkm)


@worker_router.message(Form.place_)
async def technology(message: Message, state: FSMContext):
    await state.update_data(place_=message.text)
    await state.set_state(Form.res_person)
    text = _('''
✍️Mas'ul ism sharifi?
''')
    await message.answer(text)


@worker_router.message(Form.res_person)
async def technology(message: Message, state: FSMContext):
    await state.update_data(res_person=message.text)
    await state.set_state(Form.time_connect_)
    text = _('''
🕰 Murojaat qilish vaqti: 

Qaysi vaqtda murojaat qilish mumkin?
Masalan, 9:00 - 18:00
''')
    await message.answer(text)


@worker_router.message(Form.time_connect_)
async def technology(message: Message, state: FSMContext):
    await state.update_data(time_connect_=message.text)
    await state.set_state(Form.time_work)
    text = _('''
🕰 Ish vaqtini kiriting?
''')
    await message.answer(text)


@worker_router.message(Form.time_work)
async def technology(message: Message, state: FSMContext):
    await state.update_data(time_work=message.text)
    await state.set_state(Form.salary_)
    text = _('''
💰 Maoshni kiriting?
''')
    await message.answer(text)


@worker_router.message(Form.salary_)
async def technology(message: Message, state: FSMContext):
    await state.update_data(salary_=message.text)
    await state.set_state(Form.addition_)
    text = _('''
‼️ Qo`shimcha ma`lumotlar?
''')
    await message.answer(text)


@worker_router.message(Form.addition_)
async def addition(message: Message, state: FSMContext):
    await state.update_data(addition_=message.text)
    if message.from_user.username:
        username = '@' + message.from_user.username
    else:
        username = message.from_user.full_name
    data = await state.get_data()
    await state.clear()

    text = _('''
{key}:

🏢 Idora: {office}
📚 Texnologiya: {technology_}
🇺🇿 Telegram: {username}  
📞 Aloqa: +{call}
🌐 Hudud:{place_}
✍️ Mas'ul: {res_person}
🕰 Murojaat vaqti: {time_connect_}
🕰 Ish vaqti: {time_work} 
💰 Maosh: {salary_}
‼️ Qo`shimcha: {addition_}

#ishJoyi
'''.format(key=data['key'], office=data['office'], technology_=data['technology_'],
           username=username, call=data['call'], place_=data['place_'], res_person=data['res_person'],
           time_connect_=data['time_connect_'], time_work=data['time_work'], salary_=data['salary_'],
           addition_=data['addition_']))
    await state.update_data(text=text)
    await message.answer(text, reply_markup=yes_no())
    await message.answer(_("Barcha ma'lumotlar to'g'rimi?"))
