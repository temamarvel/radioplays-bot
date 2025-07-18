import os

import telebot
import requests

from dotenv import load_dotenv
from telebot.types import InputMediaPhoto

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
            #todo maybe we need to do some stuff here
            bot.send_message(message.chat.id, "Ничего не найдено.")
            return

        for item in results:
            title = item.get("name", "Без названия")
            cover_urls = item.get("cover_urls")
            # audio_url = item.get("audio_url")

            # # Отправляем обложку
            if cover_urls:
                cover_images = list(map(lambda url:InputMediaPhoto(url, f"ph1", show_caption_above_media=True), cover_urls))
                cover_images[0].caption = title
                bot.send_media_group(message.chat.id, media=cover_images)
            else:
                bot.send_message(message.chat.id, title)
            #
            # # Отправляем аудио
            # if audio_url:
            #     bot.send_audio(message.chat.id, audio=audio_url)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при поиске: {e}")

# temp solution for MVP
bot.infinity_polling()


