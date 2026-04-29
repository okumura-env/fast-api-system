from pydantic import BaseModel, Field

# ===========================
# スキーマ定義
# ===========================

class InsertAndUpdateIngredientSchema(BaseModel):
    # 食材の名称のフィールドは必須です。
    name : str = Field(...,
                        description="食材の名前を入力してください。", 
                        example="トマト", min_length=1)

# 食材の情報を表すスキーマ
class IngredientSchema(InsertAndUpdateIngredientSchema):
    id: int = Field(..., 
                    description="食材を一意に識別するID番号",
                    example=123)

# レスポンスで使用する結果用スキーマ
class ResponseSchema(BaseModel):
    # 処理結果のメッセージ
    message: str = Field(...,
                        description="API操作の結果を説明するメッセージ",
                        example="食材の更新に成功しました。")