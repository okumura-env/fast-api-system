from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.recipe import InsertAndUpdateRecipeSchema, RecipeSchema, ResponseSchema
import cruds.recipe as recipe_crud
from database import get_dbsession

router = APIRouter(tags = ["Recipes"], prefix="/recipes")

# =======================================
# レシピ用のエンドポイント
# =======================================
# レシピ新規登録のエンドポイント
@router.post("/", response_model=ResponseSchema)
async def create_recipe(recipe: InsertAndUpdateRecipeSchema,
                        db_session: AsyncSession = Depends(get_dbsession)):
    try:
        # 新しいレシピをデータベースに登録
        await recipe_crud.insert_recipe(db_session, recipe)
        return ResponseSchema(message="レシピが正常に登録されました。")
    except Exception as e:
        # 登録に失敗した場合、HTTP 400エラーを返す
        raise HTTPException(status_code=400, detail="レシピの登録に失敗しました")
    
# レシピ情報全件取得のエンドポイント
@router.get("/", response_model=list[RecipeSchema])
async def get_recipes_list(db_session: AsyncSession = Depends(get_dbsession)):
    # レシピの全件取得
    recipes = await recipe_crud.get_recipes(db_session)
    return recipes

# 特定のレシピ情報取得のエンドポイント
@router.get("/{recipe_id}", response_model=RecipeSchema)
async def get_recipe_detail(recipe_id: int, db_session: AsyncSession = Depends(get_dbsession)):
    # 特定のレシピの情報取得
    recipe = await recipe_crud.get_recipe_by_id(db_session, recipe_id)
    if not recipe: 
        # レシピが見つからない場合、HTTP 404エラーを返す
        raise HTTPException(status_code=404, detail="レシピが見つかりません")
    return recipe
        
# 特定のレシピを更新するエンドポイント
@router.put("/{recipe_id}", response_model=ResponseSchema)
async def modify_recipe(recipe_id: int, recipe: InsertAndUpdateRecipeSchema,
                        db_session: AsyncSession = Depends(get_dbsession)):
    # 指定されたIdのレシピを新しいデータで更新
    update_recipe = await recipe_crud.update_recipe(db_session, recipe_id, recipe)
    if not update_recipe:
        # 更新対象が見つからない場合404エラーを返す
        raise HTTPException(status_code=404, detail="更新対象が見つかりません")
    return ResponseSchema(message="レシピが正常に更新されました")

# 特定のレシピを削除するエンドポイント
@router.delete("/{recipe_id}", response_model=ResponseSchema)
async def remove_recipe(recipe_id: int, db_session: AsyncSession = Depends(get_dbsession)):
    # 指定されたIDのレシピをデータベースから削除
    result = await recipe_crud.delete_recipe(db_session, recipe_id)
    if not result:
        # 削除対象が見つからない場合、HTTP 404エラーを返す
        raise HTTPException(status_code=404, detail="削除対象が見つかりません")
    return ResponseSchema(message="レシピが正常に削除されました")