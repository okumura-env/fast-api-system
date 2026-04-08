from  pydantic import BaseModel, Field

# ===========================
# スキーマ定義
# ===========================

# 登録・更新で使用するスキーマ
class InsertAndUpdateTagSchema(BaseModel):
    # タグのタイトルこのフィールドは必須です。
    title: str = Field(...,
                    description="タグのタイトルを入力してください。",
                    example="和食", min_length=1)

#タグの情報を表すスキーマ
class TagSchema(InsertAndUpdateTagSchema):
    # タグの一意識別子
    tag_id: int = Field(...,
                        description="タグを一意に識別するID番号",
                        example=123)

# レスポンスで使用する結果用スキーマ
class ResponseSchema(BaseModel):
    # 処理結果のメッセージ
    message: str = Field(...,
                        description="API操作の結果を説明するメッセージ",
                        example="タグの更新に成功しました。")
