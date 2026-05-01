from __future__ import annotations  
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import schemas.tag as tag_schema
from models.tag import Tag
from datetime import datetime

# ============================
# 非同期CRUD処理
# ============================
# 新規登録
async def insert_tag(
    db_session: AsyncSession,
    tag_data: tag_schema.InsertAndUpdateTagSchema) -> Tag:
    """
        新しいタグをデータベースに登録する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
            tag_data (InsertAndUpdateTagSchema): 作成するタグのデータ
        Returns:
            Tag: 作成されたタグのモデル
    """
    print("==== 新規登録：開始 ===")
    new_tag = Tag(**tag_data.model_dump())
    db_session.add(new_tag)
    await db_session.commit()
    await db_session.refresh(new_tag)
    print(">>>データ追加完了")
    return new_tag

# 全件取得
async def get_tags(db_session: AsyncSession) -> list[Tag]:
    """
        データベースから全てのタグを取得する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
        Returns:
            list[Tag]: 取得された全てのタグのリスト
    """
    print("=== 全件取得：開始 ===")
    result = await db_session.execute(select(Tag))
    tags = result.scalars().all()
    print(">>> データ全件取得完了")
    return tags

# 1件取得
async def get_tag_by_id(db_session: AsyncSession,
                        tag_id: int) -> Tag | None:
    """
        データベースから特定のタグを1件取得する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
            tag_id (int): 取得するタグのID(プライマリキー)
        Returns:
            Tag | None: 取得されたタグのモデル、タグが存在しない場合はNoneを返す
    """
    print("=== 1件取得：開始 ===")
    result = await db_session.execute(
        select(Tag).where(Tag.id == tag_id))
    tag = result.scalars().first()
    print(">>> データ取得完了")
    return tag

# 更新処理
async def update_tag(
        db_session: AsyncSession,
        tag_id: int,
        target_data: tag_schema.InsertAndUpdateTagSchema) -> Tag | None:
    """
        データベースのタグを更新する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
            tag_id (int): 更新するタグのID(プライマリキー)
            target_data(InsertAndUpdateTagSchema): 更新するデータ
        Returns:
            Tag | None: 更新されたタグのモデル、タグが存在しない場合はNoneを返す
    """
    print("=== データ更新：開始 ===")
    tag = await get_tag_by_id(db_session, tag_id)
    if tag:
        tag.title = target_data.title
        tag.updated_at = datetime.now()
        await db_session.commit()
        await db_session.refresh(tag)
        print(">>>データ更新完了")

    return tag


# 削除処理
async def delete_tag(
        db_session: AsyncSession, tag_id: int
        ) -> Tag | None:
    """
        データベースのタグを削除する関数
        Args:
            db_session(AsyncSession): 非同期DBセッション
            tag_id(int): 削除するタグのID(プライマリキー)
        Returns:
            Tag | None: 削除されたタグのモデル、タグが存在しない場合はNoneを返す
    """
    print("=== データ削除：開始 ===")
    tag = await get_tag_by_id(db_session, tag_id)
    if tag :
        await db_session.delete(tag)
        await db_session.commit()
        print(">>>データ削除完了")

    return tag