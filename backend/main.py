from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from fastapi.middleware.cors import CORSMiddleware
from routers.tag import router as tag_router
from routers.recipe import router as recipe_router
from routers.ingredient import router as ingredient_router
from routers.user import router as user_router

# テーブルを自動作成
app = FastAPI(title="レシピ管理API", version="1.0.0")

# CORS設定（Vue開発サーバーからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tag_router)
app.include_router(user_router)   
app.include_router(recipe_router)  
app.include_router(ingredient_router)  
    
@app.get("/")
def root():
    return {"message": "レシピ管理API へようこそ！"}


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