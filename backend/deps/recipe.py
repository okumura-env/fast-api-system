from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from usecases.recipe.create import RecipeCreateUseCase
from usecases.recipe.update import RecipeUpdateUseCase
from database import get_dbsession


# =======================================
# DIプロバイダ：RecipeCreateUseCase を組み立てる
# =======================================
def get_recipe_create_usecase(
    db_session: AsyncSession = Depends(get_dbsession),
) -> RecipeCreateUseCase:
    """RecipeCreateUseCaseのインスタンスを返す DI プロバイダ"""
    return RecipeCreateUseCase(db_session)

# =======================================
# DIプロバイダ：RecipeUpdateUseCase を組み立てる
# =======================================
def get_recipe_update_usecase(
    db_session: AsyncSession = Depends(get_dbsession),
) -> RecipeUpdateUseCase:
    """RecipeUpdateUseCaseのインスタンスを返す DI プロバイダ"""
    return RecipeUpdateUseCase(db_session)


# =======================================
# 型エイリアス：ルーター側で `repo: RecipeCreateUseCaseDep` と書くだけで UseCase が注入される
# =======================================
RecipeCreateUseCaseDep = Annotated[RecipeCreateUseCase, Depends(get_recipe_create_usecase)]
RecipeUpdateUseCaseDep = Annotated[RecipeUpdateUseCase, Depends(get_recipe_update_usecase)]
