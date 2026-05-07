from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.recipe import RecipeService
from database import get_dbsession

# =======================================
# DIプロバイダ：RecipeService を組み立てる
# =======================================
def get_recipe_service(
    db_session: AsyncSession = Depends(get_dbsession),
) -> RecipeService:
    """RecipeServiceのインスタンスを返す DI プロバイダ"""
    return RecipeService(db_session)