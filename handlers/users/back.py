from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main_key import main_menu

from loader import dp


@dp.message_handler(lambda message: message.text == "🔙 Orqaga", state="*")
async def back(message: types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
            pass
    await message.answer("Bosh menyu", reply_markup=main_menu)
