import telebot
import threading
import time
from flask import Flask

# ==========================================
# ১. টোকেন ও চ্যানেল কনফিগারেশন
# ==========================================
BOT_TOKEN_B = "8415434242:AAHrmGo44HAh_3ZtSX8x9MQh7bQkVXfQTQ0"  # ফাইল স্টোর বট
BOT_TOKEN_A = "8831702053:AAEOGLVJXwJx-zZLmDufyHO_nG5Qpy0ESSM"  # মেইন বট

CHANNEL_ID = -1003665423521  # আপনার প্রাইভেট ব্যাকআপ চ্যানেল

bot_b = telebot.TeleBot(BOT_TOKEN_B)
bot_a = telebot.TeleBot(BOT_TOKEN_A)

# ==========================================
# ২. বট ২৪ ঘণ্টা অনলাইন রাখার জন্য Flask Web Server
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# ==========================================
# ৩. বট B (File Store Bot) - শুধু ডিরেক্ট লিংক দেবে
# ==========================================
@bot_b.message_handler(commands=['start'])
def start_b(message):
    bot_b.reply_to(message, "ভিডিও বা ফাইল সেন্ড করুন, আমি শুধু ডিরেক্ট লিংক দিয়ে দেব।")

@bot_b.message_handler(content_types=['video', 'document', 'photo', 'animation'])
def handle_media_b(message):
    try:
        # ভিডিওটি চ্যানেলে ব্যাকআপ সেভ হবে
        sent_msg = bot_b.copy_message(
            chat_id=CHANNEL_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        
        movie_code = sent_msg.message_id
        bot_a_username = bot_a.get_me().username
        
        # শুধু মাত্র সরাসরি ক্লিক করার মত ডিরেক্ট লিংক
        direct_link = f"https://t.me/{bot_a_username}?start={movie_code}"

        # অন্য কোনো লেখা ছাড়া শুধু লিংকটি সেন্ড করবে
        bot_b.reply_to(message, direct_link)
        
    except Exception as e:
        bot_b.reply_to(message, f"❌ সমস্যা হয়েছে: {e}")

def run_bot_b():
    print("🤖 Bot B চালু হয়েছে...")
    while True:
        try:
            bot_b.polling(non_stop=True, interval=1, timeout=60)
        except Exception as e:
            print(f"Bot B error: {e}")
            time.sleep(3)

# ==========================================
# ৪. বট A (Main Bot) - লিংক এ ক্লিক করলে ভিডিও দেবে
# ==========================================
@bot_a.message_handler(commands=['start'])
def start_a(message):
    command_args = message.text.split()
    
    # ইউজার যদি ডিরেক্ট লিংকে ক্লিক করে আসে (যেমন: /start 15)
    if len(command_args) > 1:
        movie_code = command_args[1].strip()
        send_video_by_code(message.chat.id, movie_code)
    else:
        bot_a.reply_to(message, "👋 স্বাগতম! ভিডিও পেতে সঠিক লিংকে ক্লিক করুন।")

@bot_a.message_handler(func=lambda message: True)
def handle_text_a(message):
    movie_code = message.text.strip()
    send_video_by_code(message.chat.id, movie_code)

def send_video_by_code(chat_id, movie_code):
    if movie_code.isdigit():
        try:
            bot_a.copy_message(
                chat_id=chat_id,
                from_chat_id=CHANNEL_ID,
                message_id=int(movie_code)
            )
        except Exception:
            bot_a.send_message(chat_id, "❌ ফাইলটি পাওয়া যায়নি বা মুছে ফেলা হয়েছে!")
    else:
        bot_a.send_message(chat_id, "❌ ফাইল পেতে সঠিক লিংকে ক্লিক করুন।")

def run_bot_a():
    print("🤖 Bot A চালু হয়েছে...")
    while True:
        try:
            bot_a.polling(non_stop=True, interval=1, timeout=60)
        except Exception as e:
            print(f"Bot A error: {e}")
            time.sleep(3)

# ==========================================
# ৫. একসাথে সবকিছু চালানো
# ==========================================
if __name__ == '__main__':
    # ওয়েবসাইট সার্ভার চালু রাখা (২৪ ঘণ্টা অন রাখার জন্য)
    threading.Thread(target=run_flask, daemon=True).start()
    
    # দুটি বট চালু করা
    threading.Thread(target=run_bot_b, daemon=True).start()
    threading.Thread(target=run_bot_a, daemon=True).start()
    
    print("🚀 সবকিছু সফলভাবে চালু হয়েছে এবং ২৪ ঘন্টা অন থাকার জন্য রেডি!")
    
    # মেইন থ্রেড ধরে রাখা
    while True:
        time.sleep(1)
