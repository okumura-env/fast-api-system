from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import InsertAndUpdateUserSchema, UserSchema, ResponseSchema
import cruds.user as user_crud
from database import get_dbsession

router = APIRouter(tags=["Users"], prefix="/users")

# ===================================
# ユーザー用のエンドポイント
# ===================================
# ユーザー新規登録のエンドポイント
@router.post("/", response_model=ResponseSchema)
async def create_user(user: InsertAndUpdateUserSchema,
                    db_session: AsyncSession = Depends(get_dbsession)):
    try:
        # 新しいユーザーをデータベースに登録
        await user_crud.insert_user(db_session, user)
        return ResponseSchema(message="ユーザーが正常に登録されました")
    except Exception as e:
        # 登録に失敗した場合、HTTP 400エラーを返す
        raise HTTPException(status_code=400, detail="ユーザーの登録に失敗しました")
    
# ユーザー情報全件取得のエンドポイント
@router.get("/", response_model=list[UserSchema])
async def get_users_list(db_session: AsyncSession = Depends(get_dbsession)):
    # 全てのユーザーをデータベースから取得
    users = await user_crud.get_users(db_session)
    return users

# 特定のユーザー情報取得のエンドポイント
@router.get("/{user_id}", response_model=UserSchema)
async def get_user_detail(user_id: int,
                         db_session: AsyncSession = Depends(get_dbsession)):
    # 指定されたIDのユーザーをデータベースから取得
    user = await user_crud.get_user_by_id(db_session, user_id)
    if not user:
        # ユーザーが見つからない場合、HTTP 404エラーを返す
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    return user

# 特定のユーザーを更新するエンドポイント
@router.put("/{user_id}", response_model=ResponseSchema)
async def modify_user(user_id: int, user: InsertAndUpdateUserSchema,
                    db_session: AsyncSession = Depends(get_dbsession)):
    # 指定されたIDのユーザーを新しいデータで更新
    updated_user = await user_crud.update_user(db_session, user_id, user)
    if not updated_user:
        # 更新対象が見つからない場合404エラーを返す
        raise HTTPException(status_code=404, detail="更新対象が見つかりません")
    return ResponseSchema(message="ユーザーが正常に更新されました")

# 特定のユーザーを削除するエンドポイント
@router.delete("/{user_id}", response_model=ResponseSchema)
async def remove_user(user_id: int,
                    db_session: AsyncSession = Depends(get_dbsession)):
    # 指定されたIDのユーザーをデータベースから削除
    result = await user_crud.delete_user(db_session, user_id)
    if not result:
        # 削除対象が見つからない場合、HTTP 404エラーを返す
        raise HTTPException(status_code=404, detail="削除対象が見つかりません")
    return ResponseSchema(message="ユーザーが正常に削除されました")
