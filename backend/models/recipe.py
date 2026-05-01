from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Recipe(Base):
    # テーブル名
    __tablename__="recipes"
    # レシピID：PK：自動インクリメント
    id= Column(Integer, primary_key=True, autoincrement=True)
    # ユーザーID：投稿者
    user_id= Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="recipes")
    # タイトル：未入力不可
    title = Column(String(50), nullable=False)
    # 詳細
    description = Column(String(50))
     # 何人前
    servings = Column(Integer)
    # 作成日時
    created_at = Column(DateTime, default=datetime.now)
    # 更新日時
    updated_at = Column(DateTime)
    
    #relation
    tags = relationship("Tag", secondary="recipe_tags", back_populates="recipes")

    recipe_ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
    ingredients = relationship("Ingredient", secondary="recipe_ingredients", viewonly=True)