import pytest
from sqlalchemy import select                                                                                        
                                                                
from models import Tag


@pytest.mark.asyncio
async def test_db_fixture_works(test_session):
    """fixture 経由で in-memory DB に対して INSERT → SELECT できる確認"""                                            
    # 初期状態は空                                                                                                   
    result = await test_session.execute(select(Tag))                                                                 
    assert result.scalars().all() == []                                                                              
                                                                
    # Tag を1件 INSERT                                                                                               
    test_session.add(Tag(title="テストタグ"))
    await test_session.commit()                                                                                      
                                                                
    # SELECT で取り出せる                                                                                            
    result = await test_session.execute(select(Tag))
    tags = result.scalars().all()                                                                                    
    assert len(tags) == 1                                       
    assert tags[0].title == "テストタグ"