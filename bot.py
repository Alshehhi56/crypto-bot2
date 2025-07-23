import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Store the last portfolio value globally
last_value = 61238.76  # Example starting value

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔁 Recalculate", callback_data="recalc"))
    bot.send_message(message.chat.id, "🤖 Bot is live!", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "ℹ️ Use /portfolio to view your current portfolio value.")

@bot.message_handler(commands=['portfolio'])
def portfolio(message):
    send_portfolio(message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "recalc")
def recalc_callback(call):
    send_portfolio(call.message.chat.id)

def send_portfolio(chat_id):
    global last_value
    new_value = 61238.76  # Simulated; replace with real calculation
    change = ((new_value - last_value) / last_value) * 100

    result = "f📊 *Your Portfolio Value:* ${new_value:,.2f}"
    if abs(change) >= 5:
        direction = "📈 Increased" if change > 0 else "📉 Decreased"
        result += f"

{direction} by {abs(change):.2f}%"

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔁 Recalculate", callback_data="recalc"))
    bot.send_message(chat_id, result, parse_mode="Markdown", reply_markup=markup)
    last_value = new_value

bot.polling()
