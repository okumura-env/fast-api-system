from __future__ import annotations  
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import schemas.ingredient as ingredient_schema
import models.ingredient as ingredient_model
from datetime import datetime

# ============================
# 非同期CRUD処理
# ============================
# 新規登録
async def insert_ingredient(
    db_session: AsyncSession,
    ingredient_data: ingredient_schema.InsertAndUpdateIngredientSchema) -> ingredient_model.Ingredient:
    """
        新しい食材をデータベースに登録する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
            ingredient_data (InsertAndUpdateIngredientSchema): 作成する食材のデータ
        Returns:
            Ingredient: 作成された食材のモデル
    """
    print("==== 新規登録：開始 ===")
    new_ingredient = ingredient_model.Ingredient(**ingredient_data.model_dump())
    db_session.add(new_ingredient)
    await db_session.commit()
    await db_session.refresh(new_ingredient)
    print(">>>データ追加完了")
    return new_ingredient

# 全件取得
async def get_ingredients(db_session: AsyncSession) -> list[ingredient_model.Ingredient]:
    """
        データベースから全ての食材を取得する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
        Returns:
            list[Ingredient]: 取得された全ての食材のリスト
    """
    print("=== 全件取得：開始 ===")
    result = await db_session.execute(select(ingredient_model.Ingredient))
    ingredients = result.scalars().all()
    print(">>> データ全件取得完了")
    return ingredients

# 1件取得
async def get_ingredient_by_id(db_session: AsyncSession,
                        ingredient_id: int) -> ingredient_model.Ingredient | None:
    """
        データベースから特定の食材を1件取得する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
            ingredient_id (int): 取得する食材のID(プライマリキー)
        Returns:
            Ingredient | None: 取得された食材のモデル、食材が存在しない場合はNoneを返す
    """
    print("=== 1件取得：開始 ===")
    result = await db_session.execute(
        select(ingredient_model.Ingredient).where(ingredient_model.Ingredient.id == ingredient_id))
    ingredient = result.scalars().first()
    print(">>> データ取得完了")
    return ingredient

# 更新処理
async def update_ingredient(
        db_session: AsyncSession,
        ingredient_id: int,
        target_data: ingredient_schema.InsertAndUpdateIngredientSchema) -> ingredient_model.Ingredient | None:
    """
        データベースの食材を更新する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
            ingredient_id (int): 更新する食材のID(プライマリキー)
            target_data(InsertAndUpdateIngredientSchema): 更新するデータ
        Returns:
            Ingredient | None: 更新された食材のモデル、食材が存在しない場合はNoneを返す
    """
    print("=== データ更新：開始 ===")
    ingredient = await get_ingredient_by_id(db_session, ingredient_id)
    if ingredient:
        ingredient.name = target_data.name
        ingredient.updated_at = datetime.now()
        await db_session.commit()
        await db_session.refresh(ingredient)
        print(">>>データ更新完了")

    return ingredient


# 削除処理
async def delete_ingredient(
        db_session: AsyncSession, ingredient_id: int
        ) -> ingredient_model.Ingredient | None:
    """
        データベースの食材を削除する関数
        Args:
            db_session(AsyncSession): 非同期DBセッション
            ingredient_id(int): 削除する食材のID(プライマリキー)
        Returns:
            Ingredient | None: 削除された食材のモデル、食材が存在しない場合はNoneを返す
    """
    print("=== データ削除：開始 ===")
    ingredient = await get_ingredient_by_id(db_session, ingredient_id)
    if ingredient :
        await db_session.delete(ingredient)
        await db_session.commit()
        print(">>>データ削除完了")

    return ingredient