from pydantic import BaseModel, Field
from typing import Optional, List

# ===========================
# スキーマ定義
# ===========================

# ネスト埋め込み専用（id付き, 中間テーブルを持つため）   
class TagBase(BaseModel):                                                                                 
    id: int                                                                                                                                  
    title: str
    model_config = {"from_attributes": True}       

# 登録・更新で使用するスキーマ
class InsertAndUpdateTagSchema(BaseModel):
    # タグのタイトルこのフィールドは必須です。
    title: str = Field(...,
                    description="タグのタイトルを入力してください。",
                    example="和食", min_length=1)

#タグの情報を表すスキーマ
class TagSchema(InsertAndUpdateTagSchema):
    # タグの一意識別子
    id: int = Field(...,
                        description="タグを一意に識別するID番号",
                        example=123)
    
    model_config = {"from_attributes": True}

# レスポンスで使用する結果用スキーマ
class ResponseSchema(BaseModel):
    # 処理結果のメッセージ
    message: str = Field(...,
                        description="API操作の結果を説明するメッセージ",
                        example="タグの更新に成功しました。")
