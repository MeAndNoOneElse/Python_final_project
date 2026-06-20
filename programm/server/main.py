from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .db.database import Base, engine
from .api.api import api_router

# --- Основное приложение FastAPI ---
app = FastAPI()

# Путь к собранному фронтенду
STATIC_FILES_DIR = Path(__file__).resolve().parent.parent / "web/dist"

# CORS нужен для WebApp (preflight OPTIONS запросы к /api/*)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

# --- События жизненного цикла ---
@app.on_event("startup")
async def startup_event():
    """Создает таблицы в БД при старте."""
    # В реальном проекте здесь лучше использовать миграции Alembic
    Base.metadata.create_all(bind=engine)

# --- Подключение роутеров ---
app.include_router(api_router)

# --- Монтирование статики ---
# Этот роут должен быть одним из последних!
# Он будет обслуживать все запросы, которые не совпали с API роутами выше.
# html=True означает, что для путей вроде / или /groups он будет автоматически
# отдавать index.html, что идеально для React Router.
if STATIC_FILES_DIR.exists():
    # Для всех остальных маршрутов (кроме /api) - возвращаем index.html
    @app.get("/{path:path}", include_in_schema=False)
    async def serve_spa(path: str):
        """Serve SPA (Single Page Application) routes"""
        # Не обслуживаем /api запросы здесь
        if path.startswith('api/'):
            return {"error": "Not found"}

        # Проверяем есть ли конкретный файл
        candidate = STATIC_FILES_DIR / path
        if candidate.exists() and candidate.is_file():
            return FileResponse(candidate)

        # Для всех остальных - возвращаем index.html (React Router обработает)
        return FileResponse(STATIC_FILES_DIR / "index.html")

    # Корневой маршрут
    @app.get("/", include_in_schema=False)
    async def root():
        return FileResponse(STATIC_FILES_DIR / "index.html")
else:
    # Этот блок нужен, если вы вдруг захотите запустить бэкенд без фронтенда
    @app.get("/")
    async def read_root():
        return {"message": "Frontend not built. Run 'npm run build' in the 'web' directory."}
