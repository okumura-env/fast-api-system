from __future__ import annotations                                                                                                                                                                                                                                                               
from datetime import datetime                                   
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession                                                                                                                                                                                                                                                  
import schemas.tag as tag_schema
from models.tag import Tag                                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                                                

class TagRepository:                                                                                                                                                                                                                                                                             
    """タグのDB操作をまとめたリポジトリ。学習用。クラス化したらどうなるか確認したいだけ"""                      
                                                                                                                                                                                                                                                                                                
    def __init__(self, db_session: AsyncSession):
        # コンストラクタで依存（db_session）を受け取って保持する                                                                                                                                                                                                                                 
        self.db_session = db_session                                                                                                                                                                                                                                                             

    async def insert(                                                                                                                                                                                                                                                                            
        self, tag_data: tag_schema.InsertAndUpdateTagSchema     
    ) -> Tag:                                                                                                                                                                                                                                                                          
        new_tag = Tag(**tag_data.model_dump())        
        self.db_session.add(new_tag)                                                                                                                                                                                                                                                             
        await self.db_session.commit()
        await self.db_session.refresh(new_tag)                                                                                                                                                                                                                                                   
        return new_tag                                          
                                                                                                                                                                                                                                                                                                
    async def get_all(self) -> list[Tag]:
        result = await self.db_session.execute(select(Tag))                                                                                                                                                                                                                            
        return result.scalars().all()                           
                                                                                                                                                                                                                                                                                                
    async def get_by_id(self, tag_id: int) -> Tag | None:
        result = await self.db_session.execute(                                                                                                                                                                                                                                                  
            select(Tag).where(Tag.id == tag_id)
        )                                                                                                                                                                                                                                                                                        
        return result.scalars().first()
                                                                                                                                                                                                                                                                                                
    async def update(                                           
        self,
        tag_id: int,
        target_data: tag_schema.InsertAndUpdateTagSchema,
    ) -> Tag | None:                                                                                                                                                                                                                                                                   
        tag = await self.get_by_id(tag_id)  # 自分のメソッドを self 経由で呼べる
        if tag:                                                                                                                                                                                                                                                                                  
            tag.title = target_data.title                       
            tag.updated_at = datetime.now()                                                                                                                                                                                                                                                      
            await self.db_session.commit()                      
            await self.db_session.refresh(tag)
        return tag
                                                                                                                                                                                                                                                                                                
    async def delete(self, tag_id: int) -> Tag | None:
        tag = await self.get_by_id(tag_id)                                                                                                                                                                                                                                                       
        if tag:                                                 
            await self.db_session.delete(tag)
            await self.db_session.commit()                                                                                                                                                                                                                                                       
        return tag