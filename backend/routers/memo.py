from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.memo import InsertAndUpdateTagSchema, TagSchema, ResponseSchema
import cruds.tag as tag_crud
import db

router = APIRouter(tags=["Tags"], prefix="/tags")


# =======================================
# タグ用のエンドポイント
# =======================================
# タグ新規登録のエンドポイント
@router.post("/", response_model=ResponseSchema)
async def create_tag(tag: InsertAndUpdateTagSchema, 
                     db: AsyncSession = Depends(db.get_dbsession)):
    try:
        # 新しいメモをデータベースに登録
        await tag_crud.insert_tag(db, tag)
        return ResponseSchema(message="タグが正常に登録されました")
    except Exception as e:
        # 登録に失敗した場合、HTTP 400エラーを返す
        raise HTTPException(status_code=400, detail="タグの登録に失敗しました")

        