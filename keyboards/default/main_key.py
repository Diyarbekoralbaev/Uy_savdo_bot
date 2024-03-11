from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🏠 Sotish"),
            KeyboardButton(text="🏠 Sotib olish"),
        ],
        [
            KeyboardButton(text="Ijaraga berish"),
            KeyboardButton(text="Ijaraga olish"),
        ],
        [
            KeyboardButton(text="Profile"),
            KeyboardButton(text="📞 Aloqa"),
        ]
    ],
    resize_keyboard=True
)

RM = ReplyKeyboardRemove()

apartment_type = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Kvartira"),
            KeyboardButton(text="Dacha"),
            KeyboardButton(text="Do'kon"),
            KeyboardButton(text="Yer uchastka"),
        ],
        [
            KeyboardButton(text="🔙 Orqaga")
        ]
    ],
    resize_keyboard=True
)

contact = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True),
            KeyboardButton(text="🔙 Orqaga")
        ]
    ],
    resize_keyboard=True
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔙 Orqaga")
        ]
    ],
    resize_keyboard=True
)

sotib_olish = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔔 Obuna bo'lish"),
        ],
        [
            KeyboardButton(text="🔙 Orqaga")
        ]
    ],
    resize_keyboard=True
)

subscription_type = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔓 Bepul"),
            KeyboardButton(text="💳 Premium"),
        ],
        [
            KeyboardButton(text="🔙 Orqaga")
        ]
    ],
    resize_keyboard=True
)