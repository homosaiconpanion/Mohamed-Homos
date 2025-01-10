from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from difflib import SequenceMatcher

# قاعدة بيانات الأسئلة الرياضية
sports_questions = {
    "من هو أفضل لاعب كرة قدم في العالم؟": "أفضل لاعب يختلف حسب الآراء، لكن ليونيل ميسي وكريستيانو رونالدو هما الأكثر شهرة.",
    "كم عدد اللاعبين في فريق كرة القدم؟": "يتكون فريق كرة القدم من 11 لاعبًا.",
    "من هو هداف كأس العالم 2022؟": "كيليان مبابي هو هداف كأس العالم 2022.","كس امك": "كسمين امك.",
    "يا ابن الوسخة": "امك محتاجة نسخة.",
    "يا ابن المتناكة": "امك حكاكة.",
    "قول بلاك": "بلاك.",
    "ابوك حكاك": "انت منيوك يسطا.",
    "قول طاسة": "طاسة.",
    "امك رقاسة": "انت تتمنيك علي."
}

# وظيفة مقارنة النصوص لتجنب الرد على النصوص المتشابهة جزئيًا
def find_best_match(user_question):
    highest_ratio = 0
    best_match = None
    for question in sports_questions:
        ratio = SequenceMatcher(None, user_question, question).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = question
    return best_match, highest_ratio

# وظيفة بدء المحادثة
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("مرحبًا! اسألني أي سؤال رياضي أو أرسل عملية حسابية (مثل 5 + 3).")

# وظيفة الرد على الأسئلة
async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_question = update.message.text.strip()

    # التحقق إذا كان السؤال هو عملية حسابية
    try:
        # تقييم العملية الحسابية
        result = eval(user_question)
        await update.message.reply_text(f"نتيجة العملية: {result}")
        return
    except:
        pass

    # العثور على أفضل تطابق للسؤال
    best_match, ratio = find_best_match(user_question)
    if ratio >= 0.8:  # الرد فقط إذا كان التطابق 80% أو أكثر
        answer = sports_questions[best_match]
    else:
        answer = "عذرًا، لا أملك إجابة لهذا السؤال الآن."
    await update.message.reply_text(answer)

def main():
    # توكن البوت الخاص بك
    TELEGRAM_TOKEN = "7896633616:AAEXnrXA8lJucGghu2iNCcirEubWlC8T6zQ"

    # إعداد التطبيق
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # إضافة الأوامر والمعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))

    # تشغيل البوت
    application.run_polling()

if __name__ == "__main__":
    main()
