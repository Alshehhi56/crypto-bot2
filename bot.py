import os
import json
import time
import telebot
import threading
import requests
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import matplotlib.pyplot as plt

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN environment variable not set")

bot = telebot.TeleBot(TOKEN)
USER_ID = None  # will be set on first command

# Portfolio holdings
portfolio = {
    "optimism": 10769.03,
    "injective-protocol": 569.88,
    "filecoin": 2875.83,
    "celo": 20695.4,
    "beamx": 962658,
    "celestia": 3522.45,
    "cosmos": 1498.42,
    "pyth-network": 58373.4
}

value_history = []
previous_value = None
alerts_enabled = True

def fetch_prices():
    ids = ','.join(portfolio.keys())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    response = requests.get(url)
    return response.json()

def get_portfolio_value():
    prices = fetch_prices()
    total = 0
    for coin_id, amount in portfolio.items():
        price = prices.get(coin_id, {}).get("usd", 0)
        total += amount * price
    return round(total, 2)

def make_pie_chart():
    prices = fetch_prices()
    labels = []
    values = []
    for coin_id, amount in portfolio.items():
        price = prices.get(coin_id, {}).get("usd", 0)
        value = amount * price
        labels.append(coin_id)
        values.append(value)
    plt.figure(figsize=(6,6))
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title("Portfolio Allocation")
    plt.tight_layout()
    path = "chart.png"
    plt.savefig(path)
    plt.close()
    return path

def make_line_chart():
    timestamps = [entry["timestamp"] for entry in value_history]
    values = [entry["value"] for entry in value_history]
    if not timestamps or not values:
        return None
    plt.figure(figsize=(8,4))
    plt.plot(timestamps, values, marker='o')
    plt.title("Portfolio Value Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    path = "line_chart.png"
    plt.savefig(path)
    plt.close()
    return path

def monitor_portfolio():
    global previous_value
    while True:
        try:
            value = get_portfolio_value()
            value_history.append({"timestamp": datetime.now().strftime("%H:%M"), "value": value})
            if previous_value:
                change = ((value - previous_value) / previous_value) * 100
                if abs(change) >= 5 and alerts_enabled and USER_ID:
                    text = f"📢 *Alert!* Your portfolio changed by {change:+.2f}%\n💰 New Value: ${value:,.2f}"
                    bot.send_message(USER_ID, text, parse_mode='Markdown')
            previous_value = value
        except Exception as e:
            print("Monitor error:", e)
        time.sleep(3600)  # every hour

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global USER_ID
    USER_ID = message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📊 Recalculate Portfolio", callback_data="recalculate"))
    bot.send_message(message.chat.id, "Welcome! Use the button below to check your portfolio value.", reply_markup=markup)

@bot.message_handler(commands=['summary'])
def summary(message):
    global previous_value
    value = get_portfolio_value()
    text = f"📊 *Portfolio Value:* ${value:,.2f}"
    if previous_value:
        change = ((value - previous_value) / previous_value) * 100
        text += f"\n📈 Change: {change:+.2f}%"
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['holdings'])
def holdings(message):
    prices = fetch_prices()
    lines = []
    total = 0
    for coin_id, amount in portfolio.items():
        price = prices.get(coin_id, {}).get("usd", 0)
        value = amount * price
        total += value
        lines.append(f"{coin_id}: ${value:,.2f}")
    lines.append(f"\n💼 *Total:* ${total:,.2f}")
    bot.send_message(message.chat.id, "\n".join(lines), parse_mode='Markdown')

@bot.message_handler(commands=['alerts'])
def toggle_alerts(message):
    global alerts_enabled
    alerts_enabled = not alerts_enabled
    status = "enabled" if alerts_enabled else "disabled"
    bot.send_message(message.chat.id, f"🔔 Alerts are now *{status}*", parse_mode='Markdown')

@bot.message_handler(commands=['chart'])
def send_chart(message):
    path = make_pie_chart()
    with open(path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['history'])
def send_history_chart(message):
    path = make_line_chart()
    if path:
        with open(path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, "No history available yet.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global previous_value
    if call.data == "recalculate":
        value = get_portfolio_value()
        text = f"📊 *Your Portfolio Value:* ${value:,.2f}"
        if previous_value:
            change = ((value - previous_value) / previous_value) * 100
            if abs(change) >= 5:
                text += f"\n⚠️ *Change:* {change:+.2f}%"
        previous_value = value
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')

# Start background monitoring
threading.Thread(target=monitor_portfolio, daemon=True).start()

print("Bot is running...")
bot.polling()