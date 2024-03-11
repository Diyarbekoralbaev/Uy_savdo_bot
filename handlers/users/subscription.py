from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from states.states import Start, Subscription
from database.database import *
from keyboards.default.main_key import main_menu, sotib_olish, subscription_type, back

from loader import dp, bot
from data.config import ADMINS


@dp.message_handler(lambda message: message.text == "🔔 Obuna bo'lish")
async def subscription(message: types.Message):
    await message.answer("Obuna turini tanlang:", reply_markup=subscription_type)
    await Subscription.subscription.set()


@dp.message_handler(state=Subscription.subscription)
async def get_subscription(message: types.Message, state: FSMContext):
    if message.text == "🔓 Free":
        await message.answer("Siz bepul obuna bo'ldingiz!", reply_markup=main_menu)
        add_subscription(user_id=message.from_user.id, subscription_type="free")
        await state.finish()
    elif message.text == "💳 Premium":
        if check_user_subscription(user_id=message.from_user.id) == "premium":
            await message.answer("Siz allaqachon premium obuna bo'lgansiz!", reply_markup=main_menu)
            await state.finish()

        await Subscription.verification.set()
        await message.answer("Pullik obuna bolish uchun pulni 9860 0101 2109 1846 kartasiga jo'nating va tasdiqlashni bosing", reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="⃣ T Tasdiqlash")
                ],
                [
                    KeyboardButton(text="🔙 Orqaga")
                ]
            ],
            resize_keyboard=True
        ))
    elif message.text == "🔙 Orqaga":
        await message.answer("Bosh menyu", reply_markup=main_menu)
        await state.finish()
    else:
        await message.answer("Iltimos, tanlang!", reply_markup=subscription_type)
        await Subscription.subscription.set()


@dp.message_handler(lambda message: message.text == "⃣ T Tasdiqlash", state=Subscription.verification)
async def send_photo_for_check(message: types.Message):
    await message.answer("Tolovni tasdiqlash uchun chek rasmini yuboring!", reply_markup=back)
    await Subscription.photo.set()

# @dp.callback_query_handler(text="payyy", state=Subscription.photo)
# async def send_photo_for_checkk(call: types.CallbackQuery, state: FSMContext):
#     # Log to see if this is being called
#     print(f"Received callback for payment verification from {call.from_user.id}")
#     await call.message.answer("Tolovni tasdiqlash uchun chek rasmini yuboring!")
#     await Subscription.verification.set()


@dp.message_handler(state=Subscription.photo, content_types=types.ContentTypes.PHOTO)
async def get_photo_for_check(message: types.Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    user_phone = get_user(message.from_user.id)[2]
    await message.answer("Tolov tasdiqlanmoqda...\nAdminstratorlarimiz tez orada siz bilan bog'lanishadi!", reply_markup=main_menu)
    await bot.send_photo(chat_id=ADMINS, photo=message.photo[-1].file_id, caption=f"{message.from_user.full_name} obuna uchun to'lov qildi!\n\nTelefon raqami: {user_phone}", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"adm_verify?user_id={message.from_user.id}")
            ],
            [
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="adm_not_verify")
            ]
        ]
    ))

    await state.finish()

@dp.callback_query_handler(lambda call: call.data.startswith("adm_verify"), state="*")
async def adm_verify(call: types.CallbackQuery, state: FSMContext):
    user_id = int(call.data.split("=")[1])
    if call.from_user.id == ADMINS:
        await call.answer(cache_time=60)
        await call.message.answer("To'lov tasdiqlandi!")
        change_subscription_type(user_id=user_id, subscription_type="premium")
        await bot.send_message(chat_id=user_id, text="To'lov tasdiqlandi!\nSiz premium obuna bo'ldingiz!", reply_markup=main_menu)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.message.text}\n\nTo'lov tasdiqlandi!", reply_markup=main_menu)
        await state.finish()

    else:
        await call.answer(cache_time=60)
        await call.message.answer("Sizda bunday huquq yo'q!")
        await state.finish()


# @dp.callback_query_handler(text="adm_verify", state="*")
# async def adm_verify(call: types.CallbackQuery, state: FSMContext):
#     if call.from_user.id == ADMINS:
#         await call.answer(cache_time=60)
#         await call.message.answer("To'lov tasdiqlandi!")
#         change_subscription_type(user_id=call.message.chat.id, subscription_type="premium")
#         await bot.send_message(chat_id=call.message.chat.id, text="To'lov tasdiqlandi!\nSiz premium obuna bo'ldingiz!", reply_markup=main_menu)
#         await state.finish()
#
#     else:
#         await call.answer(cache_time=60)
#         await call.message.answer("Sizda bunday huquq yo'q!")

@dp.callback_query_handler(text="adm_not_verify", state="*")
async def adm_not_verify(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id == ADMINS:
        data = await state.get_data()
        await call.answer(cache_time=60)
        await call.message.answer("To'lov tasdiqlanmadi!")
        await bot.send_message(chat_id=call.message.chat.id, text="To'lov tasdiqlanmadi!\nSiz premium obuna bo'lmadingiz! Iltimos qaytadan urinib ko'ring", reply_markup=main_menu)
        await state.finish()
    else:
        await call.answer(cache_time=60)
        await call.message.answer("Sizda bunday huquq yo'q!")
        await state.finish()