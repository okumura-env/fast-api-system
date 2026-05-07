from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from usecases.recipe.create import RecipeCreateUseCase
from usecases.recipe.update import RecipeUpdateUseCase
from services.recipe import RecipeService
from database import get_dbsession
from deps.services.recipe import get_recipe_service 

# =======================================
# DIプロバイダ：RecipeCreateUseCase を組み立てる
# =======================================
def get_recipe_create_usecase(
    db_session: AsyncSession = Depends(get_dbsession),
    service: RecipeService = Depends(get_recipe_service)  
) -> RecipeCreateUseCase:
    """RecipeCreateUseCaseのインスタンスを返す DI プロバイダ"""
    return RecipeCreateUseCase(db_session,service)

# =======================================
# DIプロバイダ：RecipeUpdateUseCase を組み立てる
# =======================================
def get_recipe_update_usecase(
    db_session: AsyncSession = Depends(get_dbsession),
    service: RecipeService = Depends(get_recipe_service)  
) -> RecipeUpdateUseCase:
    """RecipeUpdateUseCaseのインスタンスを返す DI プロバイダ"""
    return RecipeUpdateUseCase(db_session, service)

# =======================================
# 型エイリアス：ルーター側で `repo: RecipeCreateUseCaseDep` と書くだけで UseCase が注入される
# =======================================
RecipeCreateUseCaseDep = Annotated[RecipeCreateUseCase, Depends(get_recipe_create_usecase)]
RecipeUpdateUseCaseDep = Annotated[RecipeUpdateUseCase, Depends(get_recipe_update_usecase)]
