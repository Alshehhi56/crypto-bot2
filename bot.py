import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Load the token from environment variable
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN environment variable not set")

bot = telebot.TeleBot(TOKEN)

# Store the previous portfolio value in memory
previous_value = None

def get_portfolio_value():
    # Replace this with real portfolio logic
    return 61238.76

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
        result = f"📊 *Your Portfolio Value:* ${new_value:,.2f}"
        if previous_value is not None:
            change = ((new_value - previous_value) / previous_value) * 100
            if abs(change) >= 5:
                result += f"\n⚠️ *Change:* {change:+.2f}%"
        previous_value = new_value
        bot.send_message(call.message.chat.id, result, parse_mode='Markdown')

print("Bot is running...")
bot.polling()