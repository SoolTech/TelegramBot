import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ------------------------
# ضع التوكنات تاعك هنا
TELEGRAM_TOKEN = "7839005312:AAE6YNBz11K2pYrbOW61J0Bvkok5A2t5Myc"
HF_TOKEN = "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"
MODEL_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
# ------------------------

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلا! ابعثلي أي وصف نصنعلك صورة بالذكاء الاصطناعي.")

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text

    await update.message.reply_text("⏳ جاري إنشاء الصورة...")

    response = requests.post(MODEL_URL, headers=headers, json={"inputs": prompt})

    if response.status_code == 200:
        image_bytes = response.content
        await update.message.reply_photo(photo=image_bytes, caption="✅ ها هي الصورة تاعك")
    else:
        await update.message.reply_text("❌ صرات مشكلة في التوليد. جرب وصف آخر.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))

    app.run_polling()

if __name__ == "__main__":
    main()