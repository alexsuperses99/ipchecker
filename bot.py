import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

# Укажите ваш токен
BOT_TOKEN = "8081566164:AAEjd_dFGM9hW6CbM6sM_jp85j73L0WkaCw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь /check <IP>, чтобы узнать информацию об IP-адресе.")

async def check_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Пожалуйста, укажите IP-адрес. Пример: /check 8.8.8.8")
        return

    ip = context.args[0]
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()

        if data['status'] == 'fail':
            await update.message.reply_text(f"Ошибка: {data['message']}")
        else:
            info = (
                f"IP: {data['query']}\n"
                f"Страна: {data['country']}\n"
                f"Регион: {data['regionName']}\n"
                f"Город: {data['city']}\n"
                f"Провайдер: {data['isp']}\n"
                f"Координаты: {data['lat']}, {data['lon']}"
            )
            await update.message.reply_text(info)
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")

def main():
    if not BOT_TOKEN:
        print("Ошибка: Токен бота не задан!")
        return

    # Создаем приложение
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Добавляем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_ip))

    # Запускаем бота
    app.run_polling()

if __name__ == "__main__":
    main()
