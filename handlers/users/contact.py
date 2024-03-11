from aiogram import types
from keyboards.default.main_key import main_menu

from loader import dp

@dp.message_handler(lambda message: message.text == "📞 Aloqa")
async def contact(message: types.Message):
    await message.answer(""
                         "📞 Biz bilan bog'lanish:\n\n"
                         "📱 Telefon: +998 94 373 79 49  yoki  +998 88 321 80 32\n"
                         "💬 Telegram: @AlisolihCoder    yoki   @AmrullohNurilloyev\n"
                         , reply_markup=main_menu)
