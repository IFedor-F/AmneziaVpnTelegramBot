import os

import qrcode
import telebot

import generate
from Config import TgConfig

API_TOKEN = os.getenv('TELEGRAM_FRACTAL_API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)


# Команда /generate
@bot.message_handler(commands=['generate'])
def handle_generate(message):
    if message.from_user.id not in TgConfig.admin_ids:
        return
    args = message.text.split()[1:]

    if len(args) == 0:
        bot.reply_to(message, "Enter comment")
        return

    comment = " ".join(args)
    data = generate.add_user(comment)
    bot.reply_to(message, f"```ini\n{data}\n```", parse_mode="Markdown")
    qr_img = qrcode.make(data)
    qr_img.save("new_user_qr_code.png")

    with open("awg_userconfig.ini", 'w', encoding="UTF-8") as file:
        file.write(data)

    with open("awg_userconfig.ini", 'rb') as file:
        bot.send_document(message.chat.id, file)

    with open("new_user_qr_code.png", "rb") as file:
        bot.send_photo(message.chat.id, file)

    os.remove("new_user_qr_code.png")
    os.remove("awg_userconfig.ini")


bot.polling(none_stop=True)
