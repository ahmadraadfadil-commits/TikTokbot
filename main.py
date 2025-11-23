BOT_TOKEN = "5938139554:AAGHqW4h-0NKPAWaS00X2JhwmhHnl52KeHs"

bot = telebot.TeleBot(BOT_TOKEN)

def get_tiktok_video(url):
    # نستخدم هنا واجهة برمجية (API) عامة ومجانية لجلب الفيديو بدون علامة مائية
    # ملاحظة: الخدمات المجانية قد تتوقف أحياناً، لكن هذه تعمل حالياً
    api_url = f"https://www.tikwm.com/api/?url={url}"
    try:
        response = requests.get(api_url).json()
        if response['code'] == 0:
            video_url = response['data']['play']
            title = response['data']['title']
            return video_url, title
    except Exception as e:
        print(e)
    return None, None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً! أرسل لي رابط تيك توك وسأقوم بتحميله لك بدون علامة مائية.")

@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    url = message.text
    
    # التأكد من أن الرابط من تيك توك
    if "tiktok.com" in url:
        msg = bot.reply_to(message, "جارٍ التحميل... ⏳")
        
        video_url, caption = get_tiktok_video(url)
        
        if video_url:
            try:
                # إرسال الفيديو
                bot.send_video(message.chat.id, video_url, caption=caption)
                bot.delete_message(message.chat.id, msg.message_id) # حذف رسالة الانتظار
            except Exception as e:
                bot.edit_message_text("حدث خطأ أثناء إرسال الفيديو (قد يكون حجمه كبيراً جداً).", message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("لم أتمكن من العثور على الفيديو، تأكد من صحة الرابط.", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "الرجاء إرسال رابط تيك توك صحيح.")

print("Bot is running...")
bot.infinity_polling()
