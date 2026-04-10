from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.tag import InsertAndUpdateTagSchema, TagSchema, ResponseSchema
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

# メモ情報全件取得のエンドポイント
@router.get("/", response_model=list[TagSchema])
async def get_tags_list(db: AsyncSession = Depends(db.get_dbsession)):
    # 全てのメモをデータベースから取得
    tags = await tag_crud.get_tags(db)
    return tags

# 特定のタグ情報取得のエンドポイント
@router.get("/{tag_id}", response_model=TagSchema)
async def get_tag_detail(tag_id: int,
                        db: AsyncSession = Depends(db.get_dbsession)):
    #指定されたIDのタグをデータベースから取得
    tag = await tag_crud.get_tag_by_id(db,tag_id)
    if not tag:
        # メモが見つからない場合、HTTP 404エラーを返す
        raise HTTPException(status_code=404, detail ="メモが見つかりません")
    return tag

# 特定のメモを更新するエンドポイント
@router.put("/{tag_id}", response_model=ResponseSchema)
async def modify_tag(tag_id: int, tag: InsertAndUpdateTagSchema,
                    db: AsyncSession = Depends(db.get_dbsession)):
    # 指定されたIDのメモを新しいデータで更新
    updated_tag = await tag_crud.update_tag(db, tag_id, tag)
    if not updated_tag:
        # 更新対象が見つからない場合404エラーを返す
        raise HTTPException(status_code=404, detail="更新対象が見つかりません")
    return ResponseSchema(message="メモが正常に更新されました")

# 特定のメモを削除するエンドポイント
@router.delete("/{memo_id}", response_model=ResponseSchema)
async def remove_tag(tag_id: int, 
                    db: AsyncSession = Depends(db.get_dbsession)):
    # 指定されたIDのタグをデータベースから削除
    result = await tag_crud.delete_tag(db, tag_id)
    if not result:
        # 削除対象が見つからない場合、HTTP 404エラーを返す
        raise HTTPException(status_code=404, detail="削除対象が見つかりません")
    return ResponseSchema(message="タグが正常に削除されました")
