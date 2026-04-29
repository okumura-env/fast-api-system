from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class RecipeTag(Base):
    # テーブル名
    __tablename__ = 'recipe_tags'
    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)

    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)