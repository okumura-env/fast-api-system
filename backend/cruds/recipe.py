from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import schemas.recipe as recipe_schema
from models.recipe import Recipe
from models.tag import Tag
from datetime import datetime
from sqlalchemy.orm import selectinload

# ============================
# 非同期CRUD処理
# ============================
# 新規登録
# async def insert_recipe(
#     db_session: AsyncSession,
#     recipe_data: recipe_schema.InsertAndUpdateRecipeSchema) -> Recipe:
#     """
#         新しいレシピをデータベースに登録する関数
#         Args:
#             db_session (AsyncSession): 非同期DBセッション
#             recipe_data (InsertAndUpdateRecipeSchema): 作成するレシピのデータ
#         Returns:
#             Recipe: 作成されたレシピのモデル
#     """
#     print(" === 新規登録・開始 ===")
#     result_tags = await db_session.execute(                                                                                                                                                                                                                                                           
#         select(Tag).where(Tag.id.in_(recipe_data.tag_ids))
#     )                                                                                                                                                                                                                                                                                            
#     tags = result_tags.scalars().all() 

#     result_ingredients = await db_session.execute(                                                                                                                                                                                                                                                           
#         select(Ingredient).where(Ingredient.id.in_(recipe_data.ingredient_ids))
#     )    
#     ingredients = result_ingredients.scalars().all()  

#     new_recipe = Recipe(**recipe_data.model_dump(exclude={"tag_ids", "ingredients"}))
#     new_recipe.tags = tags
#     db_session.add(new_recipe)
#     await db_session.commit()
#     await db_session.refresh(new_recipe)
#     print(">>>データ追加完了")
#     return new_recipe

# 全件取得
async def get_recipes(
    db_session:AsyncSession) -> list[Recipe]:
    """
        データベースからすべてのレシピを取得する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
        Returns:
            list[Recipe]: 取得されたすべてのレシピのリスト
    """
    print("=== 全件取得：開始 ===")
    result = await db_session.execute(select(Recipe).options(selectinload(Recipe.tags)))
    recipes = result.scalars().all()
    print(">>>データ全件取得完了")
    return recipes

# 1件取得
async def get_recipe_by_id (
    db_session:AsyncSession,
    recipe_id: int) -> Recipe | None:
    """
        データベースから特定のレシピを1件取得する関数
        Args: 
            db_session (AsyncSession): 非同期DBセッション
        Returns:
            Recipe | None: 取得されたレシピのモデル、レシピが存在しない場合はNoneを返す
    """
    print("=== 1件取得：開始 ===")
    result = await db_session.execute(
        select(Recipe).where(Recipe.id == recipe_id).options(selectinload(Recipe.tags)))
    recipe = result.scalars().first()
    print(">>> データ取得完了")
    return recipe

# 更新処理
async def update_recipe(
    db_session: AsyncSession,
    recipe_id: int,
    recipe_data: recipe_schema.InsertAndUpdateRecipeSchema) -> Recipe:
    """
        データベースのレシピを更新する関数
        Args: 
            db_session (AsyncSession): 非同期DBセッション
            recipe_id (int): 更新するレシピのID(プライマリキー)
            recipe_data (InsertAndUpdateRecipeSchema): 更新するデータ
        Returns:
            Recipe: 更新したレシピのモデル
    """
    print("=== データ更新：開始 ===")
    recipe = await get_recipe_by_id(db_session, recipe_id)
    if recipe:
        result = await db_session.execute(select(Tag).where(Tag.id.in_(recipe_data.tag_ids)))
        tags = result.scalars().all()
        recipe.user_id = recipe_data.user_id
        recipe.title = recipe_data.title
        recipe.description = recipe_data.description
        recipe.servings = recipe_data.servings
        recipe.tags = tags
        recipe.updated_at = datetime.now()
        await db_session.commit()
        await db_session.refresh(recipe)

    return recipe

# 削除処理
async def delete_recipe(
        db_session: AsyncSession,
        recipe_id: int) -> Recipe | None:
    """
        データベースのレシピを削除する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
            recipe_id (int): 削除するレシピのID(プライマリキー)
        Returns:
            Recipe | None: 削除したレシピのモデル、レシピが存在しない場合はNoneを返す
    """
    print("=== データ削除：開始 ===")
    recipe = await get_recipe_by_id(db_session, recipe_id)
    if recipe :
        await db_session.delete(recipe)
        await db_session.commit()
        print("データ削除完了")

    return recipe
