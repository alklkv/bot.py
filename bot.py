import pandas as pd
import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

# Загружаем данные
data = pd.read_excel("data.xlsx")

stations = {}
for _, row in data.iterrows():
    bs = str(row["БС"]).strip()
    name = str(row["Название"]).strip()
    try:
        lat = float(row["Широта"])
        lon = float(row["Долгота"])
        stations[bs] = {"name": name, "lat": lat, "lon": lon}
    except:
        print(f"⚠️ Пропущены некорректные координаты для БС: {bs}")

# Обработчики
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите номер БС")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    if user_input in stations:
        station = stations[user_input]
        name = station["name"]
        lat = station["lat"]
        lon = station["lon"]

        await update.message.reply_text(f"🏷 БС: {name}")
        map_url = f"https://yandex.ru/maps/?pt={lon},{lat}&z=16&l=map"
        await update.message.reply_text(f"🗺 Ссылка на карты:\n{map_url}")
    else:
        await update.message.reply_text("❌ БС не найдена.")

# Запуск бота (без закрытия loop!)
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.initialize()
    print("✅ Бот инициализирован.")
    await app.start()
    print("🚀 Бот запущен.")
    await app.updater.start_polling()
    await app.updater.wait_until_closed()
    await app.stop()
    await app.shutdown()

# Render-friendly запуск
if __name__ == "__main__":
    asyncio.run(main())
