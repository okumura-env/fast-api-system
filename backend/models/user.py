from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    # テーブル名
    __tablename__="users"
    # ユーザーID：PK：自動インクリメント
    id= Column(Integer, primary_key=True, autoincrement=True)
    # ユーザーネーム：未入力不可
    username = Column(String(50), nullable=False)

    recipes = relationship("Recipe", back_populates="user")
    # 作成日時
    created_at = Column(DateTime, default=datetime.now)
    # 更新日時
    updated_at = Column(DateTime)
    