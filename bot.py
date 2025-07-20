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
            audio_urls = item.get("audio_urls")
            cover_urls = item.get("cover_urls")

            if cover_urls:
                cover_images = list(map(lambda url:InputMediaPhoto(url, show_caption_above_media=True), cover_urls))
                cover_images[0].caption = title
                bot.send_media_group(message.chat.id, media=cover_images)
            else:
                bot.send_message(message.chat.id, title)

            # todo doesn't work on localhost. implement and test it after deploy
            # for audio_url in audio_urls:
            #     bot.send_audio(
            #         chat_id=message.chat.id,
            #         audio=audio_url,
            #         title=title,
            #         caption="Приятного прослушивания!")

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при поиске: {e}")

# temp solution for MVP
bot.infinity_polling()


