import asyncio
import uvicorn
import os
from dotenv import load_dotenv
from telegram import Update

# Загружаем переменные окружения из .env файла в корне проекта
load_dotenv()

# Импортируем приложения после загрузки .env
from server.main import app as fastapi_app

try:
    from bot.main import create_bot_app
except ImportError:
    create_bot_app = None

async def main():
    """Главная асинхронная функция для запуска FastAPI и Telegram-бота."""

    # 1. Настройка FastAPI сервера
    server_config = uvicorn.Config(
        fastapi_app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
    server = uvicorn.Server(server_config)

    bot_app = None
    webapp_task = None
    bot_task = None

    try:
        # 2. Настройка и инициализация Telegram-бота, если модуль доступен
        if create_bot_app is not None:
            try:
                bot_app = create_bot_app()
                await bot_app.initialize()
                await bot_app.start()
            except ValueError as e:
                print(f"Ошибка инициализации бота: {e}")
                bot_app = None
        else:
            print("Модуль bot не найден, запускаю только FastAPI сервер.")

        # 3. Создаем задачи для асинхронного запуска
        webapp_task = asyncio.create_task(server.serve())
        if bot_app is not None:
            bot_task = asyncio.create_task(bot_app.updater.start_polling(allowed_updates=Update.ALL_TYPES))

        print("="*50)
        print("Приложение успешно запущено!")
        print("-> FastAPI сервер работает на http://localhost:8000")
        if bot_app is not None:
            print("-> Telegram бот запущен в режиме polling.")
        else:
            print("-> Telegram бот отключен.")
        print("="*50)

        # Ожидаем завершения обеих задач.
        if bot_task is not None:
            await asyncio.gather(webapp_task, bot_task)
        else:
            await webapp_task

    except asyncio.CancelledError:
        print("\nПолучен сигнал к остановке (задачи отменены).")
    except Exception as e:
        print(f"Произошла критическая ошибка: {e}")
    finally:
        print("Начинаю корректное завершение работы...")

        # Остановка бота
        if bot_app is not None:
            try:
                if bot_app.running:
                    print("Остановка Telegram-бота (updater)...")
                    await bot_app.updater.stop()
                print("Завершение работы Telegram-бота (application)...")
                await bot_app.shutdown()
                print("Telegram-бот остановлен.")
            except Exception as e:
                print(f"Ошибка при остановке бота: {e}")

        # Отменяем и дожидаемся завершения задач
        if webapp_task and not webapp_task.done():
            webapp_task.cancel()
            try:
                await webapp_task
            except asyncio.CancelledError:
                pass

        if bot_task and not bot_task.done():
            bot_task.cancel()
            try:
                await bot_task
            except asyncio.CancelledError:
                pass

        print("Приложение полностью остановлено.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПриложение остановлено вручную.")
    except Exception as e:
        print(f"Произошла критическая ошибка на верхнем уровне: {e}")
