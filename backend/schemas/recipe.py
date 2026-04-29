from pydantic import BaseModel, Field
from typing import Optional, List
from schemas.tag import TagBase

# =====================================
# スキーマ定義
# =====================================

# 登録・更新で使用するスキーマ
# recipe_id, user_id, title, description, servings
class InsertAndUpdateRecipeSchema(BaseModel):
    # レシピの投稿者:このフィールドは必須です
    user_id: int = Field(..., 
                        description = "投稿者を一意に識別するID番号",
                        example=1)
    # レシピのタイトル:このフィールドは必須です
    title: str = Field(..., 
                        description = "タイトルを入力してください",
                        example="カレー", min_length=1)
    # レシピのタイトル:このフィールドは必須です
    description: str = Field(..., 
                        description = "詳細を入力してください",
                        example="まずは野菜を刻みます")
    # レシピは何人前か
    servings: int = Field(..., 
                        description = "何人前か入力してください",
                        example=1)
    # 紐づくtags
    tag_ids: list[int] = []
    
# レシピの情報を表すスキーマ
class RecipeSchema(InsertAndUpdateRecipeSchema):
    # レシピの一意識別子
    id: int = Field(..., 
                        description="レシピを一意に識別するID番号",
                        example=123)

    tags: Optional[List[TagBase]] = None
    model_config = {"from_attributes": True}

# レスポンスで使用する結果用スキーマ
class ResponseSchema(BaseModel):
    # 処理結果のメッセージ
    message: str = Field(...,
                        description="API操作の結果を説明するメッセージ",
                        example="レシピの更新に成功しました。")