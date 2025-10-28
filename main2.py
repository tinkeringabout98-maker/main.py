import json, requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8469043377:AAF7JHvEVGkpTVn2G2vpKXi4BlCK6PSzOH4"

# Загружаем привязанные кошельки
def load_wallets():
    try:
        with open("wallets.json", "r") as f:
            return json.load(f)
    except:
        return {}

# Сохраняем привязку
def save_wallets(wallets):
    with open("wallets.json", "w") as f:
        json.dump(wallets, f)

# Команда /link 0x...
async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    wallet = context.args[0].lower() if context.args else None
    if wallet and wallet.startswith("0x"):
        wallets = load_wallets()
        wallets[user_id] = wallet
        save_wallets(wallets)
        await update.message.reply_text(f"✅ Кошелёк {wallet[:6]}... привязан!")
    else:
        await update.message.reply_text("❌ Укажи валидный адрес: /link 0x1234...")

# Команда /topholders
async def topholders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallets = load_wallets()
    leaderboard = []
    for uid, addr in wallets.items():
        url = f"https://api.etherscan.io/api?module=account&action=balance&address={addr}&apikey=ТВОЙ_API_KEY"
        try:
            balance = int(requests.get(url).json()["result"]) / 1e18
            leaderboard.append((uid, balance))
        except:
            continue
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    msg = "🏆 Топ держателей:\n"
    for i, (uid, bal) in enumerate(leaderboard[:10], 1):
        msg += f"{i}. [user](tg://user?id={uid}) — {bal:.2f} ETH\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("link", link))
app.add_handler(CommandHandler("topholders", topholders))
app.run_polling()

requirements.txt
python-telegram-bot==20.3
requests
