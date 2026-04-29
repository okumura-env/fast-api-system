from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from schemas.ingredient import InsertAndUpdateIngredientSchema, IngredientSchema, ResponseSchema
import cruds.ingredient as ingredient_crud
from database import get_dbsession

router = APIRouter(tags=["Ingredients"], prefix="/ingredients")


# =======================================
# 食材用のエンドポイント
# =======================================
# 食材新規登録のエンドポイント
@router.post("/", response_model=ResponseSchema)
async def create_ingredient(ingredient: InsertAndUpdateIngredientSchema, 
                     db_session: AsyncSession = Depends(get_dbsession)):
    try:
        # 新しい食材をデータベースに登録
        await ingredient_crud.insert_ingredient(db_session, ingredient)
        return ResponseSchema(message="食材が正常に登録されました")
    except IntegrityError:
        # 登録に失敗した場合、HTTP 400エラーを返す
        raise HTTPException(status_code=400, detail="食材の登録に失敗しました")

# 食材情報全件取得のエンドポイント
@router.get("/", response_model=list[IngredientSchema])
async def get_ingredients_list(db_session: AsyncSession = Depends(get_dbsession)):
    # 全ての食材をデータベースから取得
    ingredients = await ingredient_crud.get_ingredients(db_session)
    return ingredients

# 特定の食材情報取得のエンドポイント
@router.get("/{ingredient_id}", response_model=IngredientSchema)
async def get_ingredient_detail(ingredient_id: int,
                        db_session: AsyncSession = Depends(get_dbsession)):
    #指定されたIDの食材をデータベースから取得
    ingredient = await ingredient_crud.get_ingredient_by_id(db_session, ingredient_id)
    if not ingredient:
        # 食材が見つからない場合、HTTP 404エラーを返す
        raise HTTPException(status_code=404, detail="食材が見つかりません")
    return ingredient

# 特定の食材を更新するエンドポイント
@router.put("/{ingredient_id}", response_model=ResponseSchema)
async def modify_ingredient(ingredient_id: int, ingredient: InsertAndUpdateIngredientSchema,
                    db_session: AsyncSession = Depends(get_dbsession)):
    # 指定されたIDの食材を新しいデータで更新
    updated_ingredient = await ingredient_crud.update_ingredient(db_session, ingredient_id, ingredient)
    if not updated_ingredient:
        # 更新対象が見つからない場合404エラーを返す
        raise HTTPException(status_code=404, detail="更新対象が見つかりません")
    return ResponseSchema(message="食材が正常に更新されました")

# 特定の食材を削除するエンドポイント
@router.delete("/{ingredient_id}", response_model=ResponseSchema)
async def remove_ingredient(ingredient_id: int,
                    db_session: AsyncSession = Depends(get_dbsession)):
    # 指定されたIDの食材をデータベースから削除
    result = await ingredient_crud.delete_ingredient(db_session, ingredient_id)
    if not result:
        # 削除対象が見つからない場合、HTTP 404エラーを返す
        raise HTTPException(status_code=404, detail="削除対象が見つかりません")
    return ResponseSchema(message="食材が正常に削除されました")
