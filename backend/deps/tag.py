from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cruds.class_tag import TagRepository
from database import get_dbsession


# =======================================
# DIプロバイダ：TagRepository を組み立てる
# =======================================
def get_tag_repository(
    db_session: AsyncSession = Depends(get_dbsession),
) -> TagRepository:
    """TagRepository のインスタンスを返す DI プロバイダ"""
    return TagRepository(db_session)


# =======================================
# 型エイリアス：ルーター側で `repo: TagRepoDep` と書くだけで Repository が注入される
# =======================================
TagRepoDep = Annotated[TagRepository, Depends(get_tag_repository)]
