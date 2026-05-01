from sqlalchemy import select                                                                                        
from sqlalchemy.ext.asyncio import AsyncSession                                                                      
from fastapi import HTTPException        

from models.tag import Tag                                                                                                        
from models.ingredient import Ingredient 

class RecipeService:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def fetch_tags_or_404(self, ids: list[int]) -> list[Tag]:  
        result = await self.db_session.execute(select(Tag).where(Tag.id.in_(ids)))
        tags = result.scalars().all()

        if len(tags) != len(set(ids)):
          raise HTTPException(status_code=404, detail="存在しないタグIDが含まれています")
        return tags


    async def fetch_ingredients_or_404(self, ids: list[int]) -> list[Ingredient]: 
        result = await self.db_session.execute(select(Ingredient).where(Ingredient.id.in_(ids)))
        ingredients = result.scalars().all()  

        if len(ingredients) != len(set(ids)):
          raise HTTPException(status_code=404, detail="存在しない食材IDが含まれています")
        return ingredients 