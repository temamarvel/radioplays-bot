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

# temp solution for MVP
bot.infinity_polling()


