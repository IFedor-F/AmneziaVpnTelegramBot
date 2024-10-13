import os
import time

import qrcode
import telebot

import generate
from Config import TgConfig

bot = telebot.TeleBot(TgConfig.API_TOKEN)


@bot.message_handler(commands=['generate'])
def handle_generate(message):
    if message.from_user.id not in TgConfig.admin_ids:
        return
    args = message.text.split()[1:]

    if len(args) < 2:
        bot.reply_to(message, "Enter config name and comment")
        return

    config_name = args[0]
    comment = " ".join(args[1:])
    try:
        data = generate.add_user(config_name, comment)
    except KeyError:
        bot.reply_to(message, "Invalid config name")
        return

    bot.reply_to(message, f"```ini\n{data}\n```", parse_mode="Markdown")
    qr_img = qrcode.make(data)
    qr_img.save("new_user_qr_code.png")

    with open("awg_userconfig.conf", 'w', encoding="UTF-8") as file:
        file.write(data)

    with open("awg_userconfig.conf", 'rb') as file:
        bot.send_document(message.chat.id, file)

    with open("new_user_qr_code.png", "rb") as file:
        bot.send_photo(message.chat.id, file)

    os.remove("new_user_qr_code.png")
    os.remove("awg_userconfig.conf")


def start_bot():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(5)


if __name__ == '__main__':
    start_bot()
