from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from bot.handlers import start, handle_menu_selection, handle_gene_name

import os
from dotenv import load_dotenv

# Загрузка токена из .env файла
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("Не найден токен бота. Убедись, что он есть в .env как BOT_TOKEN")

# Запуск бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    
    # Кнопки меню (inline)
    app.add_handler(CallbackQueryHandler(handle_menu_selection))

    # Обработка текстового ввода (названия генов)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gene_name))

    print("Бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()
