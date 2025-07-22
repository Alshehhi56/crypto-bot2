import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Store previous value in memory
previous_value = None

def get_portfolio_value():
    # Dummy value, replace with actual logic if needed
    return 61000.00

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("📊 Recalculate Portfolio", callback_data="recalculate"))
    bot.send_message(message.chat.id, "Welcome! Use the button below to check your portfolio value.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global previous_value
    if call.data == "recalculate":
        new_value = get_portfolio_value()
        if previous_value is not None:
            change = ((new_value - previous_value) / previous_value) * 100
            if abs(change) >= 5:
                bot.send_message(call.message.chat.id, f"⚠️ Portfolio changed by {change:.2f}%")
        previous_value = new_value
        result = f"📊 *Your Portfolio Value:*

💰 ${new_value:,.2f}"
        bot.send_message(call.message.chat.id, result, parse_mode='Markdown')

bot.polling()