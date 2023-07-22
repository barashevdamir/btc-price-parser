import requests
import time
from telegram import Bot
from dotenv import load_dotenv
import os
import asyncio

# Загрузка переменных окружения
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# URL API Bybit для получения последней цены биткоина
url = "https://api.bybit.com/v2/public/tickers?symbol=BTCUSDT"

# Создаем бота Telegram
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Ваша функция для получения последней цены биткоина
def get_btc_price():
    try:
        response = requests.get(url)
        data = response.json()
        return float(data['result'][0]['last_price'])
    except Exception as e:
        print(f"Error while getting price: {e}")
        return None

# Предыдущая цена для сравнения
prev_price = get_btc_price()

# Асинхронная функция
async def main_loop():
    global prev_price
    while True:
        try:
            # Задержка между запросами
            await asyncio.sleep(10)

            # Текущая цена
            current_price = get_btc_price()

            # Если не удалось получить цену, пропускаем итерацию
            if current_price is None:
                continue

            # Если цена изменилась, отправляем сообщение
            if current_price != prev_price:
                price_diff = current_price - prev_price
                message = f"Bitcoin price changed: {price_diff}"

                await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

            # Обновляем предыдущую цену
            prev_price = current_price
        except Exception as e:
            print(f"Error in main loop: {e}")

# Запуск асинхронной функции
asyncio.run(main_loop())
