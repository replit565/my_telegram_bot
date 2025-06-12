#!/usr/bin/env python3
"""
Telegram бот для Railway с работой 24/7
"""
import asyncio
import logging
import os
import time
from datetime import datetime
from flask import Flask, jsonify
import threading
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import random

# Конфигурация
BOT_TOKEN = os.environ.get('BOT_TOKEN')
PORT = int(os.environ.get('PORT', 8080))

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Счетчики
start_time = time.time()
message_count = 0

# Flask приложение для Railway
app = Flask(__name__)

@app.route('/')
def home():
    uptime = time.time() - start_time
    return f"""
    <html>
    <head><title>Mines Signal Bot</title></head>
    <body style="background:#000;color:#0f0;font-family:monospace;text-align:center;padding:50px;">
        <h1>🎯 Mines Signal Bot Active</h1>
        <p>Bot: @Mines_ChatGPT_signal_bot</p>
        <p>Uptime: {uptime:.0f} seconds</p>
        <p>Messages: {message_count}</p>
        <p>Status: ✅ Online 24/7</p>
        <p>Platform: Railway.app</p>
        <p>Последнее обновление: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "bot": "Mines_ChatGPT_signal_bot",
        "uptime": time.time() - start_time,
        "messages": message_count,
        "platform": "railway",
        "timestamp": datetime.now().isoformat()
    })

# Обработчики бота
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    global message_count
    message_count += 1
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🎯 English", callback_data="lang_en")],
        [types.InlineKeyboardButton(text="🎯 Русский", callback_data="lang_ru")]
    ])
    
    await message.answer(
        "🎯 Welcome to Mines Signal Bot!\n"
        "Choose your language:",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data.startswith('lang_'))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split('_')[1]
    
    if lang == 'ru':
        text = """🎯 Добро пожаловать в Mines Signal Bot!

📱 Регистрация:
1️⃣ Зарегистрируйтесь: https://1wxxlb.com/v3/aggressive-casino/list?p=ziuo
2️⃣ Пополните баланс минимум 100₽
3️⃣ Отправьте ID после депозита

🎮 Получайте точные сигналы для игры Mines!
✨ Работает 24/7 на Railway.app"""
    else:
        text = """🎯 Welcome to Mines Signal Bot!

📱 Registration:
1️⃣ Register: https://1wxxlb.com/v3/aggressive-casino/list?p=ziuo
2️⃣ Deposit minimum 100₽
3️⃣ Send your ID after deposit

🎮 Get accurate signals for Mines game!
✨ Running 24/7 on Railway.app"""
    
    await callback.message.edit_text(text)

@dp.message(Command("signal"))
async def send_signal(message: types.Message):
    global message_count
    message_count += 1
    
    # Случайный выбор сигнала (1-12)
    signal_num = random.randint(1, 12)
    mines_count = random.randint(3, 7)
    
    await message.answer(f"🎯 SIGNAL #{signal_num}\n💣 Mines: {mines_count}\n🎮 Good luck!")

@dp.message(Command("status"))
async def status_cmd(message: types.Message):
    global message_count
    message_count += 1
    
    uptime = time.time() - start_time
    await message.answer(
        f"📊 Bot Status\n"
        f"⏱️ Uptime: {uptime:.0f}s\n"
        f"📱 Messages: {message_count}\n"
        f"🟢 Status: Online 24/7\n"
        f"🚀 Platform: Railway.app"
    )

@dp.message()
async def handle_message(message: types.Message):
    global message_count
    message_count += 1
    
    if message.text and message.text.isdigit():
        await message.answer("✅ ID получен! Ожидайте подтверждения депозита.")
    else:
        await message.answer("📝 Отправьте ваш ID после депозита для получения сигналов.")

async def start_bot():
    """Запуск бота"""
    logger.info("Starting Telegram bot...")
    await dp.start_polling(bot)

def start_flask():
    """Запуск Flask в отдельном потоке"""
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

async def main():
    """Основная функция"""
    logger.info(f"Starting Mines Signal Bot on port {PORT}")
    logger.info("Railway.app deployment - 24/7 operation")
    
    # Запуск Flask в отдельном потоке
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # Запуск бота
    await start_bot()

if __name__ == "__main__":
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN environment variable not set")
        exit(1)
    
    asyncio.run(main())
