import telebot
from telebot import types
from flask import Flask
from threading import Thread

# সার্ভার সচল রাখার জন্য Flask setup
app = Flask('')
@app.route('/')
def home():
    return "Bot is Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# আপনার সঠিক টোকেন এবং চ্যাট আইডি
BOT_TOKEN = '8217085238:AAFSCHwLAGNxB6UFtAQ71Tt7m7q1UUA9TnA'
ADMIN_CHAT_ID = '6979733205' 

bot = telebot.TeleBot(BOT_TOKEN)

# স্টার্ট মেনু সাজানো
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("🚀 অর্ডার করুন")
    btn2 = types.KeyboardButton("💰 ব্যালেন্স চেক")
    btn3 = types.KeyboardButton("📞 সাপোর্ট")
    btn4 = types.KeyboardButton("📊 সার্ভিস পিলান")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    bot.send_message(message.chat.id, "🤖 স্বাগতম TikTok Booster BD তে!", reply_markup=markup)

# পিলান সেকশন (এখানে নিজের দামগুলো বসিয়ে নিন)
@bot.message_handler(func=lambda message: message.text == "📊 সার্ভিস পিলান")
def service_plan(message):
    prices = (
        "📊 **সার্ভিস পিলানসমূহ:**\n"
        "🔥 TikTok Followers:\n🔹 ১০০০ - ১০০ টাকা\n🔹 ৫০০০ - ৪৫০ টাকা\n\n"
        "❤️ TikTok Likes:\n🔹 ১০০০ - ৬০ টাকা\n🔹 ৫০০০ - ২৮০ টাকা"
    )
    bot.send_message(message.chat.id, prices)

# অর্ডার সেকশন
@bot.message_handler(func=lambda message: message.text == "🚀 অর্ডার করুন")
def order_instruction(message):
    msg = bot.send_message(message.chat.id, "📦 পেমেন্ট করে TrxID ও লিঙ্ক পাঠান।")
    bot.register_next_step_handler(msg, forward_to_admin)

def forward_to_admin(message):
    bot.send_message(ADMIN_CHAT_ID, f"🔔 নতুন অর্ডার এসেছে!\n👤 ইউজার: @{message.from_user.username}\n📝 তথ্য: {message.text}")
    bot.send_message(message.chat.id, "✅ আপনার অর্ডার এডমিনের কাছে পাঠানো হয়েছে।")

# সাপোর্ট ও ব্যালেন্স বাটন
@bot.message_handler(func=lambda message: message.text == "📞 সাপোর্ট")
def support(message):
    bot.send_message(message.chat.id, "সরাসরি এডমিন: @TTService_BD")

@bot.message_handler(func=lambda message: message.text == "💰 ব্যালেন্স চেক")
def balance(message):
    bot.send_message(message.chat.id, "ব্যালেন্স যোগ করতে এডমিনকে নক দিন।")

if __name__ == "__main__":
    keep_alive() # Render-এ ২৪ ঘণ্টা চালু রাখার জন্য
    bot.infinity_polling()
