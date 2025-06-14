import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters import Command
from datetime import datetime
import pytz
import os
import random
import logging
from flask import Flask
import threading

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен из переменных окружения или используем дефолтный
API_TOKEN = os.getenv('BOT_TOKEN', '8143505253:AAFxhvbvIZK4Bp4aLGJw6hH5yufzWyAOL3Q')
PORT = int(os.environ.get('PORT', 8080))

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_ids = set()
user_language = {}
confirmed_users = set()

# Flask приложение для Render
app = Flask(__name__)

@app.route('/')
def home():
    return f"""
    <html>
    <head><title>Mines Signal Bot</title></head>
    <body style="background:#000;color:#0f0;font-family:monospace;text-align:center;padding:50px;">
        <h1>🎯 Mines Signal Bot Active</h1>
        <p>Bot: @Mines_ChatGPT_signal_bot</p>
        <p>Status: ✅ Online 24/7</p>
        <p>Platform: Render.com</p>
        <p>Users: {len(confirmed_users)} confirmed</p>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return {"status": "healthy", "bot": "active"}

# --- Кнопки ---
main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📥 Регистрация"), KeyboardButton(text="📌 Инструкция")],
    [KeyboardButton(text="💬 Поддержка"), KeyboardButton(text="⚠️ Важное!")],
    [KeyboardButton(text="🎯 Получить сигнал")]
], resize_keyboard=True)

deposit_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="💳 Пополнить"), KeyboardButton(text="✅ Я пополнил")]
], resize_keyboard=True)

language_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Русский"), KeyboardButton(text="English")]
], resize_keyboard=True)

# --- Команда /start ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "🌍 Выберите язык / Select your language:",
        reply_markup=language_menu
    )

# --- Выбор языка ---
@dp.message(lambda message: message.text in ["Русский", "English"])
async def set_language(message: types.Message):
    lang = "ru" if message.text == "Русский" else "en"
    user_language[message.from_user.id] = lang
    await message.answer(
        "✅ Язык выбран. Добро пожаловать!" if lang == "ru" else "✅ Language selected. Welcome!",
        reply_markup=main_menu
    )

# --- Инструкция ---
@dp.message(lambda message: message.text == "📌 Инструкция")
async def instruction(message: types.Message):
    lang = user_language.get(message.from_user.id, "ru")
    text = (
        "1. Перейдите по ссылке\n"
        "2. Введите промокод: MONETKA50\n"
        "3. Пополните счёт от 1000 руб\n"
        "4. Введите свой ID"
    ) if lang == "ru" else (
        "1. Follow the link\n"
        "2. Enter promo code: MONETKA50\n"
        "3. Deposit at least 1000 RUB\n"
        "4. Enter your ID"
    )
    await message.answer(text)

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
    lang = user_language.get(message.from_user.id, "ru")
    text = (
        "🎰 Регистрируйся по ссылке:\n"
        "https://1wilib.life/v3/aggressive-casino?p=as47\n\n"
        "🧾 ПРИ РЕГИСТРАЦИИ ВВЕДИТЕ ПРОМОКОД: MONETKA50\n\n"
        "❗️ СТРОГО НОВЫЙ АККАУНТ 1WIN! 💥\n\n"
        "✍️ Введи свой ID:"
    ) if lang == "ru" else (
        "🎰 Register here:\n"
        "https://1wilib.life/v3/aggressive-casino?p=as47\n\n"
        "🧾 USE PROMO CODE: MONETKA50\n\n"
        "❗️ STRICTLY NEW 1WIN ACCOUNT! 💥\n\n"
        "✍️ Enter your ID:"
    )
    await message.answer(text)

# --- Обработка ID ---
@dp.message(lambda message: message.text and message.text.isdigit() and len(message.text) >= 4)
async def save_id(message: types.Message):
    user_ids.add(message.from_user.id)
    lang = user_language.get(message.from_user.id, "ru")
    text = (
        "💳 Отлично! Твой ID принят ✅\n\n"
        "🔎 Теперь внеси *тестировочный депозит* от **1000₽**, чтобы наш 🤖 ИИ увидел твой игровой аккаунт и подключился к твоему серверу 🎯\n\n"
        "🔐 Это необходимо, чтобы система могла начать выдавать тебе точные сигналы без задержек и ошибок 🧠⚡\n\n"
        "📌 После пополнения нажми кнопку 👉 «✅ Я пополнил»"
    ) if lang == "ru" else (
        "💳 Great! Your ID is accepted ✅\n\n"
        "🔎 Now make a *test deposit* of **1000₽**, so our 🤖 AI can see your gaming account and connect to your server 🎯\n\n"
        "🔐 This is necessary for the system to start giving you accurate signals without delays or errors 🧠⚡\n\n"
        "📌 After deposit, press the button 👉 «✅ Confirm deposit»"
    )
    await message.answer(text, reply_markup=deposit_menu)

# --- Кнопка Пополнить ---
@dp.message(lambda message: message.text == "💳 Пополнить")
async def deposit_link(message: types.Message):
    await message.answer("💸 Пополни счёт здесь: https://1wilib.life/v3/aggressive-casino?p=as47")

# --- Я пополнил ---
@dp.message(lambda message: message.text == "✅ Я пополнил")
async def confirm_deposit(message: types.Message):
    if message.from_user.id in user_ids:
        confirmed_users.add(message.from_user.id)
        lang = user_language.get(message.from_user.id, "ru")
        await message.answer(
            "✅ Депозит подтверждён! Теперь ты можешь получать сигналы." if lang == "ru" else "✅ Deposit confirmed! Now you can receive signals.",
            reply_markup=main_menu
        )
    else:
        lang = user_language.get(message.from_user.id, "ru")
        await message.answer(
            "⚠️ Сначала зарегистрируйся и введи свой ID!" if lang == "ru" else "⚠️ Please register and enter your ID first!"
        )

# --- Получить сигнал ---
@dp.message(lambda message: message.text == "🎯 Получить сигнал")
async def send_signal(message: types.Message):
    if message.from_user.id not in confirmed_users:
        lang = user_language.get(message.from_user.id, "ru")
        await message.answer(
            "⚠️ Чтобы получать сигналы, нужно сначала пополнить счёт и нажать «✅ Я пополнил»!" if lang == "ru" else
            "⚠️ To receive signals, you must first deposit and press «✅ Confirm deposit»!"
        )
        return

    folder_path = "screens"
    if not os.path.exists(folder_path):
        # Создаем папку если её нет
        os.makedirs(folder_path, exist_ok=True)
        await message.answer("⚠️ Скрины не найдены. Папка создана, добавьте изображения.")
        return

    files = os.listdir(folder_path)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'))]

    if not image_files:
        await message.answer("⚠️ Скрины не найдены в папке screens/")
        return

    selected_file = random.choice(image_files)
    file_path = os.path.join(folder_path, selected_file)

    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.now(moscow_tz)

    try:
        photo = FSInputFile(file_path)
        await message.answer_photo(
            photo=photo,
            caption=f"🎯 Кол-во мин: 3\n🕐 Время: {moscow_time.strftime('%H:%M:%S')} (МСК)\n⚠️ Рекомендую проигрывать каждую 5 игру чтоб не было подозрений от 1WIN 🎯"
        )
    except Exception as e:
        logger.error(f"Ошибка отправки фото: {e}")
        await message.answer("⚠️ Ошибка при отправке сигнала. Попробуйте позже.")

def start_flask():
    """Запуск Flask в отдельном потоке"""
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# --- Функция запуска бота с обработкой ошибок ---
async def run_bot():
    logger.info("🚀 Бот запускается...")
    while True:
        try:
            await dp.start_polling(bot)
        except Exception as e:
            logger.error(f"❌ Ошибка в работе бота: {e}")
            logger.info("🔄 Перезапуск через 5 секунд...")
            await asyncio.sleep(5)

# --- Запуск ---
async def main():
    # Запускаем Flask в отдельном потоке для Render
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # Запускаем бота с обработкой ошибок
    await run_bot()

if __name__ == '__main__':
    logger.info("Запуск Telegram бота для работы 24/7...")
    asyncio.run(main())
