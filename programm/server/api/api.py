from fastapi import APIRouter
from . import confirmations, debts, expenses, groups, inventory, shopping_list, stats, storage, users

api_router = APIRouter()
api_router.include_router(groups.router, prefix="/api/groups", tags=["groups"])
api_router.include_router(storage.router, prefix="/api/storage", tags=["storage"])
api_router.include_router(inventory.router, prefix="/api/inventory", tags=["inventory"])
api_router.include_router(shopping_list.router, prefix="/api/shopping-list", tags=["shopping-list"])
api_router.include_router(users.router, prefix="/api/users", tags=["users"])
api_router.include_router(expenses.router, prefix="/api/expenses", tags=["expenses"])
api_router.include_router(debts.router, prefix="/api/debts", tags=["debts"])
api_router.include_router(confirmations.router, prefix="/api/confirmations", tags=["confirmations"])
api_router.include_router(stats.router, prefix="/api/stats", tags=["stats"])
