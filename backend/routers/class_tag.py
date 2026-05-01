from fastapi import APIRouter, HTTPException, Depends                                                                                        
from sqlalchemy.ext.asyncio import AsyncSession                                                                                              
from sqlalchemy.exc import IntegrityError
from schemas.tag import InsertAndUpdateTagSchema, TagSchema, ResponseSchema                                                                  
from deps.tag import TagRepoDep
from database import get_dbsession
                                                                                                                                            
router = APIRouter(tags=["Tags"], prefix="/tags")                                                                                            

                                                                                                                                            
# =======================================                       
# タグ用のエンドポイント
# =======================================                                                                                                    
# タグ新規登録のエンドポイント
@router.post("/", response_model=ResponseSchema)                                                                                             
async def create_tag(                                           
    tag: InsertAndUpdateTagSchema,
    repo: TagRepoDep,                                                          
):                                                                                                                                           
    try:                                                                                                                                     
        await repo.insert(tag)                                                                                                               
        return ResponseSchema(message="タグが正常に登録されました")
    except IntegrityError:
        raise HTTPException(status_code=400, detail="タグの登録に失敗しました")                                                              

                                                                                                                                            
# タグ情報全件取得のエンドポイント                              
@router.get("/", response_model=list[TagSchema])
async def get_tags_list(                                                                                                                     
    repo: TagRepoDep, 
):                                                                                                                                           
    return await repo.get_all()                                 

                                                                                                                                            
# 特定のタグ情報取得のエンドポイント
@router.get("/{tag_id}", response_model=TagSchema)                                                                                           
async def get_tag_detail(                                       
    tag_id: int,
    repo: TagRepoDep, 
):                                                                                                                                           
    tag = await repo.get_by_id(tag_id)
    if not tag:                                                                                                                              
        raise HTTPException(status_code=404, detail="タグが見つかりません")
    return tag                                                                                                                               

                                                                                                                                            
# 特定のタグを更新するエンドポイント                            
@router.put("/{tag_id}", response_model=ResponseSchema)
async def modify_tag(
    tag_id: int,                                                                                                                             
    tag: InsertAndUpdateTagSchema,
    repo: TagRepoDep,                                                                                     
):                                                              
    updated_tag = await repo.update(tag_id, tag)
    if not updated_tag:                                                                                                                      
        raise HTTPException(status_code=404, detail="更新対象が見つかりません")
    return ResponseSchema(message="タグが正常に更新されました")                                                                              
                                                                                                                                            

# 特定のタグを削除するエンドポイント                                                                                                         
@router.delete("/{tag_id}", response_model=ResponseSchema)      
async def remove_tag(
    tag_id: int,                                                                                                                             
    repo: TagRepoDep, 
):                                                                                                                                           
    result = await repo.delete(tag_id)                          
    if not result:
        raise HTTPException(status_code=404, detail="削除対象が見つかりません")
    return ResponseSchema(message="タグが正常に削除されました")          