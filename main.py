import keep_alive
keep_alive.keep_alive()
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# Загрузка токена из Secrets
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@evgentests")
BOT_USERNAME = os.getenv("BOT_USERNAME", "your_bot_username")  # без @

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

cards = {
    "card_1": {
        "image": "https://postimg.cc/fVr1XPS0",
        "text": "🌿 *Зелёный человек*\nСимвол древней мудрости природы. Он напоминает о цикличности жизни и необходимости гармонии с окружающим миром. Появление этой карты указывает на время обновления и роста."
    },
    "card_2": {
        "image": "https://postimg.cc/fJkGLZJh",
        "text": "🌕 *Оборотень*\nОлицетворяет внутренние конфликты и скрытые желания. Эта карта говорит о трансформации и принятии своей теневой стороны. Возможно, настало время отпустить старые страхи и позволить себе быть настоящим."
    },
    "card_3": {
        "image": "https://postimg.cc/py0NRyVZ",
        "text": "🌊 *Келпи*\nПредупреждение о скрытых опасностях и иллюзиях. Келпи манит своей красотой, но может утащить в глубины. Будьте осторожны с тем, что кажется слишком привлекательным — за фасадом может скрываться нечто иное."
    },
    "card_4": {
        "image": "https://i.postimg.cc/d13p9jQD/Photo-Room-20250521-200551.png",
        "text": "👑 *Король эльфов*\nВоплощение власти, красоты и магии. Эта карта говорит о необходимости обратиться к своей внутренней силе и мудрости. Возможно, вы стоите на пороге важного решения, и Король эльфов предлагает вам воспользоваться своей интуицией и опытом."
    },
    "card_5": {
        "image": "https://postimg.cc/mPHKYwYX",
        "text": "🌍 *Ангел земли*\nСимвол стабильности, защиты и связи с материей. Эта карта указывает на необходимость заземления и укрепления своих позиций. Обратитесь к своим корням, найдите опору в себе и окружающем мире."
    }
}

def get_private_keyboard():
    # Кнопки для канала/группы: прямые callback
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Карта 1", callback_data='card_1'),
         InlineKeyboardButton("Карта 2", callback_data='card_2')],
        [InlineKeyboardButton("Карта 3", callback_data='card_3'),
         InlineKeyboardButton("Карта 4", callback_data='card_4')],
        [InlineKeyboardButton("Карта 5", callback_data='card_5')]
    ])

def get_callback_keyboard():
    # Кнопки для лички: обычные callback_data
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Карта 1", callback_data='card_1'),
         InlineKeyboardButton("Карта 2", callback_data='card_2')],
        [InlineKeyboardButton("Карта 3", callback_data='card_3'),
         InlineKeyboardButton("Карта 4", callback_data='card_4')],
        [InlineKeyboardButton("Карта 5", callback_data='card_5')]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отправляем сразу меню с кнопками
    await update.message.reply_photo(
        photo="https://postimg.cc/TKQZwQYs",
        caption="🌿 Выбери одну из пяти карт и получи послание от сил природы:",
        reply_markup=get_callback_keyboard()
    )

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Пост в канал с кнопками для перехода в личку
    await context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo="https://postimg.cc/TKQZwQYs",
        caption="🌿 Духи лесов, теней и ветра рядом. Волшебные создания — тоже. Они не кричат, не навязываются. Просто ждут, пока ты остановишься и услышишь их.\n\n🌒 Закрой глаза. Отпусти мысли. Смотри на карты — не умом, а тем что глубже. Какая из них тянется к тебе? Кто сегодня шепчет тебе ответ?",
        reply_markup=get_private_keyboard()
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data in cards:
        try:
            logging.info(f"Нажата кнопка: {data}")
            card = cards[data]
            logging.info(f"URL изображения: {card['image']}")
            await context.bot.send_photo(
                chat_id=user_id,
                photo=card["image"],
                caption=card["text"],
                parse_mode='Markdown'
            )
            logging.info(f"Сообщение успешно отправлено для карты {data}")
        except Exception as e:
            logging.error(f"Ошибка отправки сообщения для карты {data}: {e}")
            await query.answer("❗ Напиши боту в личку, чтобы получить послание", show_alert=True)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("post", post))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()