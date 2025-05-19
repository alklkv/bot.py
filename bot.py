import pandas as pd
import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# Загружаем Excel
data = pd.read_excel("data.xlsx")

# Словарь: БС -> {название, широта, долгота}
stations = {}
for _, row in data.iterrows():
    bs = str(row["БС"]).strip()
    name = str(row["Название"]).strip()
    try:
        lat = float(row["Широта"])
        lon = float(row["Долгота"])
        stations[bs] = {"name": name, "lat": lat, "lon": lon}
    except Exception:
        print(f"⚠️ Пропущены некорректные координаты для БС: {bs}")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите номер БС")

# Сообщения с БС
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    if user_input in stations:
        station = stations[user_input]
        lat, lon = station["lat"], station["lon"]
        name = station["name"]

        await update.message.reply_text(f"🏷 БС: {name}")
        map_url = f"https://yandex.ru/maps/?pt={lon},{lat}&z=16&l=map"
        await update.message.reply_text(f"🗺 Ссылка на карты:\n{map_url}")
    else:
        await update.message.reply_text("❌ БС не найдена. Проверь номер.")

# Инициализация и запуск
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Бот запущен...")
    await app.run_polling()

# Для совместимости с Render (и другими async-средами)
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
