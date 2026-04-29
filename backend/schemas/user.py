from pydantic import BaseModel, Field
from typing import List, Optional

# ===========================
# スキーマ定義
# ===========================

# 登録・更新で使用するスキーマ
class InsertAndUpdateUserSchema(BaseModel):
    # ユーザーネームこのフィールドは必須です。
    username: str = Field(...,
                description="ユーザーネームを入力してください。",
                example="okumura", min_length=1)

class UserSchema(InsertAndUpdateUserSchema):
   # ユーザーの一意 
   id: int = Field(...,
                        description="ユーザーを一意に識別するID番号",
                        example=1)

class ResponseSchema(BaseModel):
    # 処理結果のメッセージ
    message: str = Field(...,
                        description="API操作の結果を説明するメッセージ",
                        example="ユーザーの更新に成功しました。")