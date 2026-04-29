from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import schemas.user as user_schema
import models.user as user_model
from datetime import datetime

# ============================
# 非同期CRUD処理
# ============================
# 新規登録
async def insert_user(
    db_session: AsyncSession,
    user_data: user_schema.InsertAndUpdateUserSchema) -> user_model.User:
    """
        新しいユーザーをデータベースに登録する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
            user_data (InsertAndUpdateUserSchema): 作成するユーザーのデータ
        Returns:
            User: 作成されたユーザーのモデル
    """
    print("==== 新規登録：開始 ====")
    new_user = user_model.User(**user_data.model_dump())
    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)
    print("データ追加完了")
    return new_user

# 全件取得
async def get_users(db_session: AsyncSession) -> list[user_model.User]:
    """
        データベースから全てのユーザーを取得する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
        Returns:
            list[User]: 取得された全てのユーザーのリスト
    """
    print("=== 全件取得：開始 ===")
    result = await db_session.execute(select(user_model.User))
    users = result.scalars().all()
    print("データ全件取得完了")
    return users

# 1件取得
async def get_user_by_id(db_session: AsyncSession,
                        user_id: int) -> user_model.User | None:
    """
        データベースから特定のユーザーを1件取得する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
            user_id (int): 取得するユーザーのID(プライマリキー)
        Returns:
            User | None: 取得されたユーザーのモデル、ユーザーが存在しない場合はNoneを返す
    """
    print(" === 1件取得：開始 ===")
    result = await db_session.execute(
        select(user_model.User).where(user_model.User.id == user_id)
    )
    user = result.scalars().first()
    print(">>>データ取得完了")
    return user

# 更新処理
async def update_user(
    db_session: AsyncSession,
    user_id: int,
    target_data: user_schema.InsertAndUpdateUserSchema) -> user_model.User | None:
    """
        データベースのユーザーを更新する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
            user_id (int): 更新するユーザーのID(プライマリキー)
            target_data(InsertAndUpdateUserSchema): 更新するデータ
        Returns:
            User | None: 更新されたユーザーのモデル、ユーザーが存在しない場合はNoneを返す
    """
    print(" === データ更新：開始 === ")
    user = await get_user_by_id(db_session, user_id)
    if user:
        user.username = target_data.username
        user.updated_at = datetime.now()
        await db_session.commit()
        await db_session.refresh(user)
        print(">>>データ更新完了")

    return user

# 削除処理
async def delete_user(
    db_session: AsyncSession, user_id: int
    ) -> user_model.User | None:
    """
        データベースのユーザーを削除する関数
        Args:
            db_session(AsyncSession): 非同期DBセッション
            user_id(int): 削除するユーザーのID(プライマリキー)
        Returns:
            User | None: 削除されたユーザーのモデル、ユーザーが存在しない場合はNoneを返す
    """
    print(" === データ削除：開始 === ")
    user = await get_user_by_id(db_session, user_id)
    if user :
        await db_session.delete(user)
        await db_session.commit()
        print(">>>データ削除完了")

    return user