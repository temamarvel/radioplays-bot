import os

import telebot
import requests

from dotenv import load_dotenv

load_dotenv()

LOCAL_API_URL = "http://127.0.0.1:8000/"
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Отправь мне название аудиозаписи.")

@bot.message_handler(func=lambda message: True)
def handle_search(message):
    search_text = message.text.strip()

    try:
        response = requests.get(f"{LOCAL_API_URL}/audio/", params={"search_text": search_text})
        response.raise_for_status()
        results = response.json()

        if not results:
            bot.send_message(message.chat.id, "Ничего не найдено.")
            return

        for item in results:
            title = item.get("name", "Без названия")
            # cover_url = item.get("cover_url")
            # audio_url = item.get("audio_url")

            bot.send_message(message.chat.id, title)

            # # Отправляем обложку
            # if cover_url:
            #     bot.send_photo(message.chat.id, photo=cover_url, caption=title)
            # else:
            #     bot.send_message(message.chat.id, title)
            #
            # # Отправляем аудио
            # if audio_url:
            #     bot.send_audio(message.chat.id, audio=audio_url)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при поиске: {e}")

# temp solution for MVP
bot.infinity_polling()


