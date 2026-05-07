from __future__ import annotations
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import schemas.recipe as recipe_schema
from models.recipe import Recipe
from models.recipe_ingredient import RecipeIngredient
import cruds.recipe as recipe_crud
from services.recipe import RecipeService
from typing import Optional 

class RecipeUpdateUseCase:

    def __init__(self, db_session: AsyncSession, service: RecipeService):
        self.db_session = db_session
        self.service = service

    async def execute(self,recipe_id: int,recipe_data: recipe_schema.InsertAndUpdateRecipeSchema) -> Optional[Recipe]:
        async with self.db_session.begin():
            print("=== データ更新：開始 ===")
            recipe = await recipe_crud.get_recipe_by_id(self.db_session, recipe_id)
            if recipe:
                tags = await self.service.fetch_tags_or_404(recipe_data.tag_ids) 
                recipe.user_id = recipe_data.user_id
                recipe.title = recipe_data.title
                recipe.description = recipe_data.description
                recipe.servings = recipe_data.servings
                recipe.tags = tags

                ingredient_ids = [item.ingredient_id for item in recipe_data.ingredients]                                            
                await self.service.fetch_ingredients_or_404(ingredient_ids)   
                recipe.recipe_ingredients = [
                    RecipeIngredient(ingredient_id=item.ingredient_id, quantity=item.quantity)                                       
                    for item in recipe_data.ingredients
                ]   
                recipe.updated_at = datetime.now()

            return recipe