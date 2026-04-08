from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Tag(Base):
    # テーブル名
    __tablename__="tags"
    # メモID：PK：自動インクリメント
    tag_id= Column(Integer, primary_key=True, autoincrement=True)
    # タイトル：未入力不可
    title = Column(String(50), nullable=False)
    # 作成日時
    created_at = Column(DateTime, default=datetime.now())
    # 更新日時
    updated_at = Column(DateTime)
    