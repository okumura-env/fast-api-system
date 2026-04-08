from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from schemas.tag import InsertAndUpdateTagSchema, TagSchema, ResponseSchema
# from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine

Base.metadata.create_all(bind=engine)

# テーブルを自動作成
app = FastAPI(title="レシピ管理API", version="1.0.0")

# CORS設定（Vue開発サーバーからのアクセスを許可）
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/")
def root():
    return {"message": "レシピ管理API へようこそ！"}

# ==============================
#  タグ用のエンドポイント
# ==============================
# タグの新規登録
@app.post("/tags", response_model=ResponseSchema)
async def create_tag(tag: InsertAndUpdateTagSchema):
    print(tag)
    return ResponseSchema(messaage="タグが正常に登録されました")

# タグ情報全件取得
@app.get("/tags", response_model=list[TagSchema])
async def get_tags_list():
    return [
        TagSchema(title="タグ1", tag_id=1),
        TagSchema(title="タグ2", tag_id=2),
        TagSchema(title="タグ3", tag_id=3)
    ]

# 特定のタグ情報取得
@app.get("/tags/{tag_id}", response_model=TagSchema)
async def get_tag_detail(tag_id: int):
    return TagSchema(title="タグ1", tag_id=tag_id)

# 特定のメモを更新する
@app.put("/tags/{tag_id}", response_model=ResponseSchema)
async def update_tag(tag_id: int, tag: InsertAndUpdateTagSchema):
    print(tag_id, tag)
    return ResponseSchema(message="タグが正常に更新されました")

# 特定のメモを削除する
@app.delete("/tags/{tag_id}", response_model=ResponseSchema)
async def remove_tag(tag_id: int):
    print(tag_id)
    return ResponseSchema(message="タグが正常に削除されました")

# バリデーションエラーのカスタムハンドラ
@app.exception_handler(ValidationError)
async def validation_exception_handler(exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.model
        }
    )