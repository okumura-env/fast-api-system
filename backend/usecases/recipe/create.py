from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import schemas.recipe as recipe_schema
from models.recipe import Recipe
from models.tag import Tag
from models.recipe_ingredient import RecipeIngredient
from services.recipe import RecipeService

class RecipeCreateUseCase:

    def __init__(self, db_session: AsyncSession, service: RecipeService):
        self.db_session = db_session
        self.service = service

    async def execute(self,recipe_data: recipe_schema.InsertAndUpdateRecipeSchema) -> Recipe:
        async with self.db_session.begin():
            print(" === 新規登録・開始 ===")
            result_tags = await self.db_session.execute(                                                                                                                                                                                                                                                           
                select(Tag).where(Tag.id.in_(recipe_data.tag_ids))
            )                                                                                                                                                                                                                                                                                            
            tags = result_tags.scalars().all()  

            new_recipe = Recipe(**recipe_data.model_dump(exclude={"tag_ids", "ingredients"}))
            new_recipe.tags = tags
            new_recipe.recipe_ingredients = []

            for item in recipe_data.ingredients:
                ri = RecipeIngredient(
                    ingredient_id = item.ingredient_id,
                    quantity = item.quantity,
                )
                new_recipe.recipe_ingredients.append(ri)
            self.db_session.add(new_recipe)

            print(">>>データ追加完了")
            return new_recipe