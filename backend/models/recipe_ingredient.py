from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class RecipeIngredient(Base):
    # テーブル名
    __tablename__ = 'recipe_ingredients'
    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)

    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)

    quantity = Column(Integer)

    recipe = relationship("Recipe", back_populates="recipe_ingredients")                                            
    ingredient = relationship("Ingredient", back_populates="recipe_ingredients")  