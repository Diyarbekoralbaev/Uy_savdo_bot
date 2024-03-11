from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS, UY_KANAL
from states.states import SellApartment
from database.database import *
from keyboards.default.main_key import main_menu, RM, apartment_type, sotib_olish, back
from keyboards.inline.confirm import confirm

from loader import dp, bot


@dp.message_handler(lambda message: message.text == "🏠 Sotish")
async def sell_apartment(message: types.Message):
    await message.answer("Uy turi:", reply_markup=apartment_type)
    await SellApartment.type.set()

@dp.message_handler(state=SellApartment.type)
async def get_type(message: types.Message, state: FSMContext):
    await state.update_data(type=message.text)
    await message.answer("Uy rasmini yuboring!", reply_markup=RM)
    await SellApartment.next()


@dp.message_handler(state=SellApartment.photo, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    await message.answer("Shahar:", reply_markup=RM)
    await SellApartment.next()

@dp.message_handler(state=SellApartment.city)
async def get_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Mikrorayon:", reply_markup=RM)
    await SellApartment.next()

@dp.message_handler(state=SellApartment.area)
async def get_area(message: types.Message, state: FSMContext):
    await state.update_data(area=message.text)
    await message.answer("Manzil:", reply_markup=RM)
    await SellApartment.next()

@dp.message_handler(state=SellApartment.address)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Xonalar soni:", reply_markup=RM)
    await SellApartment.next()

@dp.message_handler(state=SellApartment.rooms)
async def get_rooms(message: types.Message, state: FSMContext):
    await state.update_data(rooms=message.text)
    await message.answer("Narxi:", reply_markup=RM)
    await SellApartment.next()

@dp.message_handler(state=SellApartment.price)
async def get_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Qo'shimcha ma'lumot:", reply_markup=RM)
    await SellApartment.next()

@dp.message_handler(state=SellApartment.additional_info)
async def get_additional_info(message: types.Message, state: FSMContext):
    await state.update_data(additional_info=message.text)
    data = await state.get_data()
    await message.answer(f"Ushbu ma'lumotlar bilan e'lon qilmoqchimisiz?\n\n"
                         f"Uy Sotiladi\n\n"
                         f"🏠 Uy turi: {data['type']}\n"
                         f"🏙 Shahar: {data['city']}\n"
                         f"🌆 Mikrorayon: {data['area']}\n"
                         f"🏠 Manzil: {data['address']}\n"
                         f"🛏 Xonalar soni: {data['rooms']}\n"
                         f"💰 Narxi: {data['price']}\n"
                         f"📝 Qo'shimcha ma'lumot: {data['additional_info']}\n\n"
                         f"E'lon qilishni tasdiqlaysizmi?", reply_markup=confirm)
    await SellApartment.check.set()

@dp.callback_query_handler(text="confirm", state=SellApartment.check)
async def confirm_listing(call: types.CallbackQuery, state: FSMContext):
    if check_user_subscription(call.from_user.id) == "premium":
        data = await state.get_data ()
        user = get_user (call.from_user.id)
        listing_id = add_listing (
            user_id=user[0],
            photo=data['photo_id'],
            type=data['type'],
            city=data['city'],
            area=data['area'],
            address=data['address'],
            rooms=data['rooms'],
            price=data['price'],
            additional_info=data['additional_info'],
            message_id=0
        )
        message = await bot.send_photo(chat_id=UY_KANAL, photo=data['photo_id'],
                                        caption=f"🔑 ID: {listing_id} \n🏠 Uy turi: {data['type']}\n🏙 Shahar: {data['city']}\n🌆 Mikrorayon: {data['area']}\n🏠 Manzil: {data['address']}\n🛏 Xonalar soni: {data['rooms']}\n💰 Narxi: {data['price']}\n📝 Qo'shimcha ma'lumot: {data['additional_info']}\n\n E'lon beruvchi: *******\n Telefon raqami: *********")
        set_message_id (listing_id, message.message_id)
        await call.message.answer ("E'lon qabul qilindi!", reply_markup=main_menu)
        await state.finish ()
    else:
        await call.message.answer ("Sizda premium obuna yo'q! Premium obuna uchun to'lovni amalga oshiring!  Obuna narxi 1000 so'm", reply_markup=sotib_olish)
        await state.finish()

@dp.callback_query_handler(text="RM", state=SellApartment.check)
async def cancel_listing(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("E'lon bekor qilindi!", reply_markup=main_menu)
    await state.finish()

# @dp.message_handler(lambda message: message.text == "🏠 Sotish")
# async def sell_apartment(message: types.Message):
#     await message.answer("Iltimos, uy rasmini yuboring!", reply_markup=back)
#     await SellApartment.type.set()
#
# @dp.message_handler(state=SellApartment.photo, content_types=types.ContentTypes.PHOTO)
# async def get_photo(message: types.Message, state: FSMContext):
#     await state.update_data(photo_id=message.photo[-1].file_id)
#     await message.answer("Uy turi:", reply_markup=apartment_type)
#     await SellApartment.next()

# @dp.message_handler(state=SellApartment.type)
# async def get_type(message: types.Message, state: FSMContext):
#     await state.update_data(type=message.text)
#     await message.answer("Shahar:", reply_markup=RM)
#     await SellApartment.next()