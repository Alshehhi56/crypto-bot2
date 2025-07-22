import telebot
from telebot import types
import requests

TOKEN = "7489134851:AAGY6r_DAkTWmtKR8wIpq3LizKSsU6etSAM"
bot = telebot.TeleBot(TOKEN)

portfolio = {
    "op": 10769.03,
    "inj": 569.88,
    "fil": 2875.83,
    "celo": 20695.4,
    "beamx": 962658,
    "tia": 3522.45,
    "atom": 1498.42,
    "pyth": 58373.4
}

def get_prices():
    ids = ",".join(["optimism", "injective-protocol", "filecoin", "celo", "onbeam", "celestia", "cosmos", "pyth-network"])
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    response = requests.get(url).json()
    return {
        "op": response["optimism"]["usd"],
        "inj": response["injective-protocol"]["usd"],
        "fil": response["filecoin"]["usd"],
        "celo": response["celo"]["usd"],
        "beamx": response["onbeam"]["usd"],
        "tia": response["celestia"]["usd"],
        "atom": response["cosmos"]["usd"],
        "pyth": response["pyth-network"]["usd"]
    }

def calculate_portfolio():
    prices = get_prices()
    total = 0
    result = "📊 *Your Portfolio Value:*\n\n

"
    for token, amount in portfolio.items():
        price = prices.get(token, 0)
        value = round(price * amount, 2)
        total += value
        result += f"- {token.upper()}: ${value:,.2f}\n"
    result += f"\n*Total:* ${total:,.2f}"
    return result

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("🔄 Recalculate Portfolio", callback_data="recalculate")
    markup.add(button)
    bot.send_message(message.chat.id, "Welcome! Use the button below to recalculate your portfolio:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "recalculate")
def handle_recalculate(call):
    text = calculate_portfolio()
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

bot.polling(non_stop=True)
