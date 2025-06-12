import web
from background import keep_alive 
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters import Command
from datetime import datetime
import pytz
import os
import random

API_TOKEN = '8143505253:AAHXz5W3-ow08qHoNX1RKmUjqu_sFjHxKOQ'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_ids = set()
user_language = {}

# --- Кнопки ---
main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📥 Регистрация"), KeyboardButton(text="📌 Инструкция")],
    [KeyboardButton(text="💬 Поддержка"), KeyboardButton(text="⚠️ Важное!")],
    [KeyboardButton(text="🎯 Получить сигнал")]
], resize_keyboard=True)

# --- Команда /start ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "🌍 Выберите язык / Select your language:",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Русский"), KeyboardButton(text="English")]
        ], resize_keyboard=True)
    )

# --- Выбор языка ---
@dp.message(lambda message: message.text in ["Русский", "English"])
async def set_language(message: types.Message):
    lang = "ru" if message.text == "Русский" else "en"
    user_language[message.from_user.id] = lang
    await message.answer("✅ Язык выбран. Добро пожаловать!" if lang == "ru" else "✅ Language selected. Welcome!", reply_markup=main_menu)

# --- Инструкция ---
@dp.message(lambda message: message.text == "📌 Инструкция")
async def instruction(message: types.Message):
    await message.answer("1. Перейдите по ссылке\n2. Введите промокод: MONETKA50\n3. Пополните счёт от 1000 руб\n4. Введите свой ID")

# --- Поддержка ---
@dp.message(lambda message: message.text == "💬 Поддержка")
async def support(message: types.Message):
    await message.answer("📩 Связь с поддержкой: @kaznet20")
# --- Важное ---
@dp.message(lambda message: message.text == "⚠️ Важное!")
async def important(message: types.Message):
    await message.answer(
        "❗️Чтобы не было подозрений от 1WIN, играйте аккуратно и проигрывайте каждую 5 игру или 6 игру в Mines.\n\n"
        "❗Почему? Если вы будете постоянно выигрывать, ваш аккаунт попадёт под подозрение. "
        "Если его проверят и найдут софт — лавочка закроется!\n\n"
        "⚠️ Соблюдайте правила для своей безопасности и сохранения аккаунта!"
    )
# --- Регистрация ---
@dp.message(lambda message: message.text == "📥 Регистрация")
async def registration(message: types.Message):
    await message.answer(
        "🎰 Регистрируйся по ссылке:\n"
        "https://1wilib.life/v3/aggressive-casino?p=as47\n\n" 
        "🧾  ПРИ РЕГИСТРАЦИИ ВВЕДИТЕ ПРОКОМОД : MONETKA50\n\n"
        "❗️ СТРОГО НОВЫЙ АККАНТ 1WIN! 💥\n"
        
        "✍️ Сделайте тестируемый депозит,чтобы бот подключился к вашему аккаунту 1WIN, и начал выдавать точные сигналы.\n"
        "❓ Введи свой ID:"
    )

@dp.message(lambda message: message.text and message.text.isdigit() and len(message.text) >= 4)
async def save_id(message: types.Message):
    user_ids.add(message.from_user.id)
    await message.answer("✅ ID принят. Теперь вы можете получать сигналы!")

# --- Получить сигнал ---
@dp.message(lambda message: message.text == "🎯 Получить сигнал")
async def send_signal(message: types.Message):
    if message.from_user.id not in user_ids:
        await message.answer("⚠️ Сначала зарегистрируйтесь и введи свой ID!")
        return

    folder_path = "screens"
    if not os.path.exists(folder_path):
        await message.answer("⚠️ Скрины не найдены.")
        return
        
    files = os.listdir(folder_path)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'))]
    
    if not image_files:
        await message.answer("⚠️ Скрины не найдены.")
        return

    selected_file = random.choice(image_files)
    file_path = os.path.join(folder_path, selected_file)

    # Получаем московское время
    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.now(moscow_tz)
    
    photo = FSInputFile(file_path)
    await message.answer_photo(
        photo=photo,
        caption=f"🎯 Кол-во мин: 3\n🕐 Время: {moscow_time.strftime('%H:%M:%S')} (МСК)\n⚠️ Рекомендую проигрывать каждую 5 игру чтоб не было подозрений от 1WIN 🎯"
    )

# --- Запуск ---
async def main():
    await dp.start_polling(bot)
    
keep_alive()
if __name__ == '__main__':
    asyncio.run(main())
app.run(host="0.0.0.0", port=8080)
