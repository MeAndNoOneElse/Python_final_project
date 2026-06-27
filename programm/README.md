# SplitChek

**SplitChek** - это веб-приложение и Telegram-бот для управления совместными расходами в группах. Проект помогает отслеживать долги, покупки и расходы между друзьями и семьей.

## О проекте

SplitChek - это полноценное решение для совместного финансового управления в группах. Проект объединяет:
- **FastAPI Backend** - сервер с REST API для обработки данных
- **Telegram Bot** - удобный доступ через мессенджер
- **React Frontend** - веб-интерфейс для просмотра данных

## Возможности

- **Управление группами** - создание и участие в группах для совместных расходов
- **Отслеживание долгов** - автоматический расчет баланса между участниками
- **История расходов** - добавление чеков и распределение расходов
- **Список покупок** - совместное управление списком покупок
- **Холодильник** - учет товаров на складах с уведомлением о низком запасе
- **Telegram бот** - удобный доступ через бота в Telegram

## Установка

### Backend (FastAPI)

```bash
cd programm/server
pip install -r requirements.txt
python main.py
```

### Frontend (React)

```bash
cd programm/web
npm install
npm run dev
```

### Telegram Bot

```bash
cd programm/bot
pip install -r requirements.txt
python main.py
```

## ⚙️ Переменные окружения

Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=sqlite:///./splitchek.db
TELEGRAM_BOT_TOKEN=your_bot_token
WEBAPP_URL=http://localhost:8000
```

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/groups` | GET, POST | Управление группами |
| `/api/users/me` | GET, PUT | Профиль пользователя |
| `/api/debts` | GET | Список долгов |
| `/api/inventory` | GET, POST | Холодильник |
| `/api/shopping-list` | GET, POST | Список покупок |
| `/api/expenses` | GET, POST | Расходы |

## 👥 Участники проекта

- **Ануфриев Андрей** - Backend, Server, Web frontend
- **Хабиб Мохаммед** - Telegram Bot

## 📄 Лицензия

MIT License

---
*Проект разработан в рамках учебы в ИТМО в 2026 году*