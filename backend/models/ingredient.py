from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Ingredient(Base):
    # テーブル名
    __tablename__="ingredients"
    # 食事ID:PK:自動インクリメント
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 名前: 未入力
    name = Column(String(50), nullable=False)
    # 作成日時
    created_at = Column(DateTime, default=datetime.now)
    # 更新日時
    updated_at = Column(DateTime)