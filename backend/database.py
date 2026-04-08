import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase

#=================
# DBアクセス
#=================

#ベースクラスの定義
class Base(DeclarativeBase):

# DBファイル作成
base_dir = os.path.dirname(__file__)
# データベースのURL
DATABASE_URL = 'sqlite+aiosqlite:///' + os.path.join(base_dir, 'tagdb.sqlite')

# 非同期エンジンの作成
engine = create_async_engine(DATABASE_URL, echo=True)

# 非同期セッションの設定
async_session = async_sessionmaker(
    engine, 
    expire_on_commit = False, 
    class_=AsyncSession
)

# DBとのセッションを非同期的に扱うことができる関数
async def get_dbsession():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except: 
            await session.rollback()
            raise