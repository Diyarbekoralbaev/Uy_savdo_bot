from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from states.states import Start
from database.database import *
from keyboards.default.main_key import main_menu

from loader import dp


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    if get_user(message.from_user.id) is None:
        await message.answer(f"Salom, {message.from_user.full_name}!\n"
                             f"Botimizga xush kelibsiz!\n"
                             f"Botimiz orqali siz xohlagan hududlarda joylashgan uy va dala hovlilarni topishingiz mumkin!\n"
                             f"Botdan foydalanish uchun telefon raqamingizni yuboring:")
        await Start.phone.set()
    else:
        await message.answer(f"Salom, {message.from_user.full_name}!\n"
                             f"Botimizga xush kelibsiz!\n"
                             f"Botimiz orqali siz xohlagan hududlarda joylashgan uy va dala hovlilarni topishingiz mumkin!\n", reply_markup=main_menu)


@dp.message_handler(state=Start.phone)
async def enter_phone(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(phone=message.text)
        try:
            add_user(message.from_user.id, message.from_user.full_name, message.text)
            add_subscription(user_id=message.from_user.id, subscription_type="free")
            await message.answer("Telefon raqamingiz qabul qilindi", reply_markup=main_menu)
        except Exception as e:
            print(e)
            await message.answer(f"Telefon raqamingiz qabul qilinmadi!")
            await Start.phone.set()
        finally:
            await state.finish()
    else:
        await message.answer("Telefon raqamingizni to'g'ri yuboring!\nFaqat raqamlar qabul qilinadi!")
        await Start.phone.set()

