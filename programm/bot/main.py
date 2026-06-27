"""
SplitChek Telegram Bot Module.

This module implements a Telegram bot for managing group expenses.
Features include:
- User profile management
- Group management
- Expense tracking
- Shopping list
- Inventory management
- NLU message processing

Author: habib
"""

import os
import re
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

DEFAULT_USER_ID = 2138544164
WEBAPP_URL = os.getenv("WEBAPP_URL", "http://localhost:8000/webapp")

# Bot version and configuration
BOT_VERSION = "1.0.0"
BOT_NAME = "SplitChek Bot"


def create_bot_app():
    """Create and configure the Telegram bot application."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env файле")

    application = Application.builder().token(token).build()

    # Личные команды
    application.add_handler(CommandHandler("start", start_private))
    application.add_handler(CommandHandler("webapp", webapp_private))
    application.add_handler(CommandHandler("groups", groups_private))
    application.add_handler(CommandHandler("debts", debts_private))
    application.add_handler(CommandHandler("status", status_private))
    application.add_handler(CommandHandler("pay", pay_handler))
    application.add_handler(CommandHandler("settings", settings_private))
    application.add_handler(CommandHandler("default_storage", default_storage))
    application.add_handler(CommandHandler("take", take_product))
    application.add_handler(CommandHandler("use", use_product))
    application.add_handler(CommandHandler("want", want_product))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))

    # Групповые команды
    application.add_handler(CommandHandler("qr", qr_command))
    application.add_handler(CommandHandler("add", add_receipt))
    application.add_handler(CommandHandler("shopping", shopping_list))
    application.add_handler(CommandHandler("storage", storage_cmd))

    # NLU - обработка сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return application


# === ЛИЧНЫЕ СООБЩЕНИЯ ===

async def start_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("🚀 Открыть SplitChek", web_app={"url": WEBAPP_URL}),
        InlineKeyboardButton("📊 Мои долги", command="debts"),
        InlineKeyboardButton("⚙️ Настройки", command="settings")
    ]]
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! 👋\n"
        "Это бот для управления совместными расходами.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def webapp_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Открыть приложение", web_app={"url": WEBAPP_URL})]]
    await update.message.reply_text(
        "Нажми на кнопку, чтобы открыть приложение:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def groups_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List user's groups - placeholder for future implementation"""
    await update.message.reply_text("Список групп пока не реализован.")


async def debts_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's debts - placeholder for future implementation"""
    await update.message.reply_text("Долги пока не реализованы.")


async def status_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's balance status - placeholder for future implementation"""
    await update.message.reply_text("Статус пока не реализован.")


async def pay_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle payment command - placeholder for future implementation"""
    await update.message.reply_text("Команда /pay: /pay [группа] [кто] [сумма]")


async def settings_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Открыть настройки", web_app={"url": f"{WEBAPP_URL}/settings"})]]
    await update.message.reply_text("Настройки:", reply_markup=InlineKeyboardMarkup(keyboard))


async def default_storage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Укажи название: /default_storage морозильник")
        return
    await update.message.reply_text(f"Холодильник по умолчанию: {' '.join(context.args)}")


async def take_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Укажи продукт: /take молоко 1л")
        return
    await update.message.reply_text(f"✅ Добавлено: {' '.join(context.args)}")


async def use_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Укажи продукт: /use молоко 0.5л")
        return
    await update.message.reply_text(f"✅ Списано: {' '.join(context.args)}")


async def want_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Укажи продукт: /want хлеб")
        return
    await update.message.reply_text(f"🛒 В списке покупок: {' '.join(context.args)}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Команды:\n"
        "/start - Меню\n"
        "/webapp - Приложение\n"
        "/debts - Долги\n"
        "/status - Баланс\n"
        "/settings - Настройки\n"
        "/help - Помощь"
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🤖 SplitChek Bot\nТвой ID: {update.effective_user.id}")


# === ГРУППОВЫЕ ЧАТЫ ===

async def qr_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text("Только в группах")
        return
    keyboard = [[InlineKeyboardButton("🚀 Сканер QR", web_app={"url": f"{WEBAPP_URL}/scanner"})]]
    await update.message.reply_text("Отсканируй чек:", reply_markup=InlineKeyboardMarkup(keyboard))


async def add_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text("Только в группах")
        return
    if len(context.args) == 0:
        await update.message.reply_text("Пример: /add молоко 89₽")
        return
    keyboard = [[InlineKeyboardButton("🔗 Открыть WebApp", web_app={"url": f"{WEBAPP_URL}/distribute"})]]
    await update.message.reply_text(f"📸 Чек: {' '.join(context.args)}", reply_markup=InlineKeyboardMarkup(keyboard))


async def shopping_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text("Только в группах")
        return
    await update.message.reply_text("🛒 Список покупок:\n- молоко\n- хлеб")


async def storage_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display group's storage contents - placeholder for future implementation"""
    if update.effective_chat.type == "private":
        await update.message.reply_text("Только в группах")
        return
    storage = context.args[0] if context.args else "основной"
    await update.message.reply_text(f"🧊 {storage}:\n- молоко: 2л\n- хлеб: 1 бутик")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle NLU message processing for group chats"""
    if update.effective_chat.type == "private":
        return
    text = update.message.text.lower()
    if "купил" in text or "взял" in text:
        await update.message.reply_text("✅ Добавлено в холодильник")
    elif "кончил" in text or "закончил" in text:
        await update.message.reply_text("🗑️ Списано")
    elif "надо купить" in text or "добавь" in text:
        await update.message.reply_text("🛒 В список покупок")