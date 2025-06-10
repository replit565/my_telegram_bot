import os
import random
import asyncio
from datetime import datetime

import pytz
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters import Command

from background import keep_alive  # keep_alive.py добавим ниже

API_TOKEN = os.getenv("BOT_TOKEN")  # Получаем токен из переменной окружения

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_ids = set()
user_language = {}
confirmed_users = set()

# --- Кнопки ---
main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📥 Регистрация"), KeyboardButton(text="📌 Инструкция")],
    [KeyboardButton(text="💬 Поддержка"), KeyboardButton(text="⚠️ Важное!")],
    [KeyboardButton(text="🎯 Получить сигнал")]
], resize_keyboard=True)

deposit_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="💳 Пополнить"), KeyboardButton(text="✅ Я пополнил")]
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
        "🧾 ПРИ РЕГИСТРАЦИИ ВВЕДИТЕ ПРОМОКОД: MONETKA50\n\n"
        "❗️ СТРОГО НОВЫЙ АККАУНТ 1WIN! 💥\n\n"
        "✍️ Введи свой ID:"
    )

# --- Обработка ID ---
@dp.message(lambda message: message.text and message.text.isdigit() and len(message.text) >= 4)
async def save_id(message: types.Message):
    user_ids.add(message.from_user.id)
    await message.answer(
        "💳 Отлично! Твой ID принят ✅\n\n"
        "🔎 Теперь внеси *тестировочный депозит* от **1000₽**, чтобы наш 🤖 ИИ увидел твой игровой аккаунт и подключился к твоему серверу 🎯\n\n"
        "🔐 Это необходимо, чтобы система могла начать выдавать тебе точные сигналы без задержек и ошибок 🧠⚡\n\n"
        "📌 После пополнения нажми кнопку 👉 «✅ Я пополнил»",
        reply_markup=deposit_menu
    )

# --- Кнопка Пополнить ---
@dp.message(lambda message: message.text == "💳 Пополнить")
async def deposit_link(message: types.Message):
    await message.answer("💸 Пополни счёт здесь: https://1wilib.life/v3/aggressive-casino?p=as47")

# --- Я пополнил ---
@dp.message(lambda message: message.text == "✅ Я пополнил")
async def confirm_deposit(message: types.Message):
    if message.from_user.id in user_ids:
        confirmed_users.add(message.from_user.id)
        await message.answer("✅ Депозит подтверждён! Теперь ты можешь получать сигналы.", reply_markup=main_menu)
    else:
        await message.answer("⚠️ Сначала зарегистрируйся и введи свой ID!")

# --- Получить сигнал ---
@dp.message(lambda message: message.text == "🎯 Получить сигнал")
async def send_signal(message: types.Message):
    if message.from_user.id not in confirmed_users:
        await message.answer("⚠️ Чтобы получать сигналы, нужно сначала пополнить счёт и нажать «✅ Я пополнил»!")
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

if __name__ == '__main__':
    keep_alive()  # Запуск web-сервера для поддержки работы на хостинге
    asyncio.run(main())
