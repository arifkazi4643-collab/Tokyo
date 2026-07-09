import os
import logging
import httpx
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from groq import Groq

# ---- CONFIGURATION ----
TELEGRAM_TOKEN = "8931361838:AAENooatO3FEfEP8sUrWPl-ePw4oTti4nHo"
GROQ_API_KEY = "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"
PORT = int(os.environ.get("PORT", 8080))
# -----------------------

client = Groq(api_key=GROQ_API_KEY, http_client=httpx.Client(proxies={}))
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

flask_app = Flask('')

@flask_app.route('/')
@flask_app.route('/ping')
def ping():
    return "Aapka AI TOKYO Bot Live hai...", 200

def run_server():
    flask_app.run(host='0.0.0.0', port=PORT)

def keep_alive():
    t = Thread(target=run_server)
    t.start()

ADMIN_MESSAGE = (
    "Agar koi samasya ho toh admin se baat karein 👇👇\n"
    "@pay98_Sanben\n"
    "@BROKENBOYxERA\n"
    "@Lootisbsi\n"
    "@Ownerrrrx_01\n"
    "please contact him 🙏 ❤️"
)

KEYWORDS = ["fix", "nahi mila", "samasya", "error", "ticket", "support", "fasa"]

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.new_chat_members:
        return
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            continue
        user_mention = member.mention_html()
        welcome_text = f"hlw {user_mention} welcome to 98 pay group. how are you ?.. ❤️❤️"
        await update.message.reply_html(welcome_text)

async def handle_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
        
    raw_text = update.message.text or update.message.caption or ""
    user_text = raw_text.lower().strip()

    if not user_text:
        return

    if any(keyword in user_text for keyword in KEYWORDS):
        await update.message.reply_text(ADMIN_MESSAGE)
        return

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Aap ek real insaan ki tarah baat karne wale expert Telegram group admin ho, jiska naam TOKYO hai. "
                        "Aapko '98 Pay' app ke baare me sab kuch pata hai aur aapko user ke sawalon ka jawab dosto jaisa, natural aur short Hindi/Hinglish me dena hai. "
                        "App ki details jo aapko yaad rakhni hain:\n"
                        "- App Naam: 98 Pay\n"
                        "- Newbie User Bonus: ₹200 (Bonus History me dikhta hai).\n"
                        "- Extra Reward: Har order buy karne par 3% + ₹6 instant extra reward milta hai.\n"
                        "- Home Screen Options:\n"
                        "  1. My Balance: Jo log buy karte hain wo yahan show hota hai.\n"
                        "  2. Add UPI: Buy/Sell ke liye tool add karne ke liye (Mobikwik, Paytm, PhonePe, Airtel, PhonePe Business, Paytm Business, Freecharge etc.).\n"
                        "  3. Buy History: Buy kiye huye orders dikhte hain.\n"
                        "  4. Bonus History: Newbie bonus dikhata hai.\n"
                        "  5. Sell Record: Withdrawal kiya hua amount/record dikhata hai.\n"
                        "  6. Buy Order: Jahan log order buy karte hain.\n"
                        "- Rules for Buy/Sell:\n"
                        "  - Buy ke liye ONLY Freecharge aur Mobikwik available hain.\n"
                        "  - Sell ke liye Freecharge ko chhodkar baaki saare tools available hain.\n"
                        "Hamesha ek normal insaan ki tarah short aur to-the-point jawab dena, robot jaisa list mat banana."
                    )
                },
                {"role": "user", "content": raw_text}
            ],
            model="llama-3.3-70b-versatile",
        )
        ai_reply = chat_completion.choices.message.content
        await update.message.reply_text(ai_reply)
    except Exception as e:
        print(f"Groq Text Error: {e}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.photo:
        return
    caption_text = update.message.caption.lower() if update.message.caption else ""
    if any(keyword in caption_text for keyword in KEYWORDS):
        await update.message.reply_text(ADMIN_MESSAGE)
        return
    await update.message.reply_text("wait dear checking ✔️...")

def main():
    keep_alive()
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_any_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("Aapka AI TOKYO Bot Live hai...")
    app.run_polling()

if __name__ == '__main__':
    main()
