from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
import calendar
import asyncio
import datetime

# === Token ===
TOKEN = "BOT_TOKEN_HERE"

# === Bot va Dispatcher ===
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# === Oy nomlari ===
month_names = [
    "Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
    "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"
]

# === /start komandasi ===
@router.message(F.text == "/start")
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📅 Bugun", callback_data="today_day")]
        ]
    )
    await message.answer(
        "Assalomu alaykum!\nQaysi yilning kalendarini ko‘rmoqchisiz?\nMasalan: 2025",
        reply_markup=keyboard
    )

# === Bugungi sana va hafta kuni ===
@router.callback_query(F.data == "today_day")
async def today_callback(call: CallbackQuery):
    weekdays = {
        0: "Dushanba",
        1: "Seshanba",
        2: "Chorshanba",
        3: "Payshanba",
        4: "Juma",
        5: "Shanba",
        6: "Yakshanba"
    }
    today = datetime.datetime.now()
    weekday = weekdays[today.weekday()]
    date_str = today.strftime("%Y-%m-%d")
    await call.message.answer(f"📌 Bugun {date_str}, {weekday}")
    await call.answer()

# === Yil kiritsa – oyma-oy kalendar yuboriladi ===
@router.message(F.text.regexp(r"^\d{4}$"))
async def calendar_handler(message: Message):
    year = int(message.text)
    cal = calendar.TextCalendar(firstweekday=0)

    for month in range(1, 13):
        month_text = cal.formatmonth(year, month)
        await message.answer(f"<b>{month_names[month - 1]} {year}</b>\n<pre>{month_text}</pre>")

# === Fallback ===
@router.message()
async def fallback(message: Message):
    await message.answer("Iltimos, faqat 4 xonali yil kiriting. Masalan: 2024")

# === Main ===
async def main():
    print("✅ Bot ishga tushdi")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
