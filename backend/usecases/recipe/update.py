from __future__ import annotations
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import schemas.recipe as recipe_schema
from models.recipe import Recipe
from models.tag import Tag
from models.recipe_ingredient import RecipeIngredient
import cruds.recipe as recipe_crud

class RecipeUpdateUseCase:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def execute(self,recipe_id: int,recipe_data: recipe_schema.InsertAndUpdateRecipeSchema) -> Optional[Recipe]:
        async with self.db_session.begin():
            print("=== データ更新：開始 ===")
            recipe = await recipe_crud.get_recipe_by_id(self.db_session, recipe_id)
            if recipe:
                result = await self.db_session.execute(select(Tag).where(Tag.id.in_(recipe_data.tag_ids)))
                tags = result.scalars().all()
                recipe.user_id = recipe_data.user_id
                recipe.title = recipe_data.title
                recipe.description = recipe_data.description
                recipe.servings = recipe_data.servings
                recipe.tags = tags
                recipe.recipe_ingredients = [
                    RecipeIngredient(ingredient_id=item.ingredient_id, quantity=item.quantity)                                       
                    for item in recipe_data.ingredients
                ]   
                recipe.updated_at = datetime.now()

            return recipe