import telebot

# Directly use the token (for testing purposes only)
TOKEN = "7489134851:AAGY6r_DAkTWmtKR8wIpq3LizKSsU6etSAM"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot is live!")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, f"You said: {message.text}")

bot.polling(non_stop=True)
