
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

portfolio = {
    "FIL": 2875.83,
    "TIA": 3522.45,
    "CELO": 20695.4,
    "PYTH": 58373.4,
    "INJ": 569.88,
    "BEAMX": 962658,
    "ATOM": 1498.42,
    "OP": 10769.03
}

initial_value = 61238.76
last_value = initial_value

def get_portfolio_value():
    # This is mock. Replace with actual price fetching logic
    prices = {
        "FIL": 2.8,
        "TIA": 2.0,
        "CELO": 0.36,
        "PYTH": 0.13,
        "INJ": 14.2,
        "BEAMX": 0.0075,
        "ATOM": 5.02,
        "OP": 0.76
    }
    total = 0
    for token, amount in portfolio.items():
        total += prices[token] * amount
    return round(total, 2)

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📊 Recalculate Portfolio", callback_data="recalculate"))
    bot.send_message(message.chat.id, "Bot is live!")
Press the button to check your portfolio value.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "recalculate")
def handle_recalculate(call):
    global last_value
    current_value = get_portfolio_value()
    change = ((current_value - last_value) / last_value) * 100

    response = f"📊 *Your Portfolio Value:*

💰 ${current_value:,.2f}"
    if abs(change) >= 1:
        response += f"
🔔 Value changed by {change:.2f}%"
    else:
        response += f"
📈 Change: {change:.2f}%"

    last_value = current_value
    bot.send_message(call.message.chat.id, response, parse_mode="Markdown")

bot.infinity_polling()
