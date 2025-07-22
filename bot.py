import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN environment variable not set")
bot = telebot.TeleBot(TOKEN)

# Store previous values per user
user_previous_values = {}

def get_portfolio_value():
    # Dummy value, replace with actual logic if needed
    return 61000.00

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("📊 Recalculate Portfolio", callback_data="recalculate"))
    bot.send_message(
        message.chat.id,
        "Welcome! Use the button below to check your portfolio value.",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    new_value = get_portfolio_value()
    previous_value = user_previous_values.get(user_id)
    if previous_value is not None:
        try:
            change = ((new_value - previous_value) / previous_value) * 100
            if abs(change) >= 5:
                bot.send_message(call.message.chat.id, f"⚠️ Portfolio changed by {change:.2f}%")
        except ZeroDivisionError:
            bot.send_message(call.message.chat.id, "Error: Previous portfolio value is zero.")
    user_previous_values[user_id] = new_value
    result = f"📊 *Your Portfolio Value:*\n\n💰 ${new_value:,.2f}"
    bot.send_message(call.message.chat.id, result, parse_mode='Markdown')

if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Bot polling failed: {e}")