from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.config import KVARTIRA_URL
from states.states import BuyApartment
from database.database import *
from keyboards.default.main_key import back, main_menu

from loader import dp

@dp.message_handler(lambda message: message.text == "Ijaraga olish")
async def buy_apartment(message: types.Message):
    await message.answer("Sotib oladigan uylar ro'yxatini ko'rish uchun quyidagi kanalga o'ting: https://t.me/+lQHZ4CW3X3NmMGEy\n\nO'zingizni qiziqtirgan uy idsini kiriting va uy haqida yashiringan malumotlarni oling", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔗 Kvartira ro'yxati", url=KVARTIRA_URL)
            ],
            [
                InlineKeyboardButton(text="🔙 Orqaga", callback_data="back")
            ]
        ]
    ))
    await BuyApartment.id.set()

@dp.message_handler(state=BuyApartment.id)
async def get_id(message: types.Message, state: FSMContext):
    if get_subscription(user_id=message.from_user.id) == "free":
        await message.answer("Sizda yashiringan malumotlarni korish uchun ruxsat yoq. Iltimos pullik obuna sotib oling!  Obuna narxi 1000 so'm")
        await state.finish()
    else:

        if message.text == "🔙 Orqaga":
            await message.answer("Bosh menyu", reply_markup=main_menu)
            await state.finish()

        elif message.text.isdigit():
            data = get_full_data_apartment(message.text)
            if data is not None:
                await message.answer(f"🔑 ID: {data['id']}\n🏠 Uy turi: {data['type']}\n🏙 Shahar: {data['city']}\n🏞 Mikrorayon: {data['area']}\n🏠 Manzil: {data['address']}\n🛏 Xonalar soni: {data['rooms']}\n💰 Narxi: {data['price']}\n📝 Qo'shimcha ma'lumot: {data['additional_info']}\n\n👤 Bino egasi: {data['owner']}\n📞 {data['phone']}", reply_markup=back)
                await BuyApartment.id.set()
            else:
                await message.answer("Bunday ID raqamli uy topilmadi!")
                await BuyApartment.id.set()
        else:
            await message.answer("ID raqamni to'g'ri kiriting!")
            await BuyApartment.id.set()
