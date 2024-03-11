from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirm = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="RM")
        ]
    ]
)
