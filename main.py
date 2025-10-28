import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔑 Токен от BotFather — обязательно в кавычках
TOKEN = "8469043377:AAF7JHvEVGkpTVn2G2vpKXi4BlCK6PSzOH4"

# 📈 Команда /price показывает курс монеты
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coin = context.args[0] if context.args else "bitcoin"
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    response = requests.get(url).json()

    if coin in response:
        rate = response[coin]["usd"]
        await update.message.reply_text(f"💰 Курс {coin.capitalize()} сейчас: ${rate}")
    else:
        await update.message.reply_text("❌ Монета не найдена. Попробуй /price bitcoin")

# 🚀 Запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("price", price))
app.run_polling()

🔹 requirements.txt

python-telegram-bot==20.3
requests
