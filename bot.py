from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# Укажите ваш токен прямо в коде
BOT_TOKEN = "8081566164:AAEjd_dFGM9hW6CbM6sM_jp85j73L0WkaCw"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Отправь /check <IP>, чтобы узнать информацию об IP-адресе.")

def check_ip(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text("Пожалуйста, укажите IP-адрес. Пример: /check 8.8.8.8")
        return

    ip = context.args[0]
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()

        if data['status'] == 'fail':
            update.message.reply_text(f"Ошибка: {data['message']}")
        else:
            info = (
                f"IP: {data['query']}\n"
                f"Страна: {data['country']}\n"
                f"Регион: {data['regionName']}\n"
                f"Город: {data['city']}\n"
                f"Провайдер: {data['isp']}\n"
                f"Координаты: {data['lat']}, {data['lon']}"
            )
            update.message.reply_text(info)
    except Exception as e:
        update.message.reply_text(f"Произошла ошибка: {str(e)}")

def main():
    if not BOT_TOKEN:
        print("Ошибка: Токен бота не задан!")
        return

    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("check", check_ip))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
