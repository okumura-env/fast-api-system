import pytest_asyncio
from sqlalchemy.ext.asyncio import (                                                                                 
    create_async_engine,                                        
    AsyncSession,                                                                                                    
    async_sessionmaker,
)                                                                                                                    
from sqlalchemy.pool import StaticPool                          

from database import Base
import models  # noqa: F401  ← 全テーブルを Base.metadata に登録するため必要
                                                                                                                    
                                                                                                                    
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"                                                                   
                                                                                                                    
                                                                
@pytest_asyncio.fixture
async def test_engine():
    """テスト用 in-memory SQLite エンジン。テストごとに新規作成・破棄。"""
    engine = create_async_engine(                                                                                    
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},                                                                   
        poolclass=StaticPool,                                                                                        
    )
    async with engine.begin() as conn:                                                                               
        await conn.run_sync(Base.metadata.create_all)           
                                                                                                                    
    yield engine
                                                                                                                    
    await engine.dispose()                                      


@pytest_asyncio.fixture
async def test_session(test_engine):
    """テスト用 AsyncSession。test_engine を流用。"""
    async_session = async_sessionmaker(                                                                              
        test_engine,
        expire_on_commit=False,                                                                                      
        class_=AsyncSession,                                    
    )                                                                                                                
    async with async_session() as session:
        yield session    

from httpx import AsyncClient, ASGITransport
                                                                                                                    
from main import app                                            
from database import get_dbsession


@pytest_asyncio.fixture
async def client(test_session):
    """get_dbsession を test_session で差し替えた HTTP クライアント"""                                               

    async def override_get_dbsession():                                                                              
        yield test_session                                      

    app.dependency_overrides[get_dbsession] = override_get_dbsession                                                 

    transport = ASGITransport(app=app)                                                                               
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac                                                                                                     

    app.dependency_overrides.clear()  