from aiogram import types
from database.database import *
from states.states import Start
from keyboards.default.main_key import sotib_olish

from loader import dp

@dp.message_handler(lambda message: message.text == "Profile")
async def profile(message: types.Message):
    data = get_user(message.from_user.id)
    subscription_info = get_subscription(message.from_user.id)
    if data:
        await message.answer(f"👤 Sizning profil ma'lumotlaringiz:\n\n"
                             f"👤 Ismingiz: {data[1]}\n"
                             f"📞 Telefon raqamingiz: {data[2]}\n"
                             f"🔔 Obuna muddati: {subscription_info[3]}\n"
                             f"🔔 Obuna turi: <b>{subscription_info[4]}</b>\n\n"
                             f"🔔 Obuna muddati tugaganida, obunani yangilash uchun 'Obuna bo'lish' tugmasini bosing! Onuna narxi 1000 so'm",
                             reply_markup=sotib_olish)
    else:
        await message.answer("Sizning profil ma'lumotlaringiz topilmadi! Iltimos, telefon raqamingizni yuboring!")
        await message.answer("📞 Telefon raqamingizni yuboring:", reply_markup=types.ReplyKeyboardRemove())
        await Start.phone.set()
