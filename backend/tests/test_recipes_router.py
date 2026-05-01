import pytest

# @pytest.mark.asyncio                                                                                                 
# async def test_put_recipe_updates_fields(client, test_session): 
#     # 1. まずレシピを1件作る                                                                                         
#     create_resp = await client.post("/recipes/", json={...})
                                                                                                                    
#     # 2. PUT で更新                                             
#     update_resp = await client.put(f"/recipes/{recipe_id}", json={...})                                              
#     assert update_resp.status_code == 200                                                                            

#     # 3. GET で更新が反映されているか確認                                                                            
#     get_resp = await client.get(f"/recipes/{recipe_id}")        
#     assert get_resp.json()["title"] == "更新後タイトル"                                                              
                                                                                                                    

@pytest.mark.asyncio                                                                                                 
async def test_put_recipe_returns_404_when_not_found(client):   
    payload = {
        "user_id": 1,                                                                                                
        "title": "存在しないレシピ",                            
        "description": "テスト",                                                                                     
        "servings": 1,                                                                                               
        "tag_ids": [],
        "ingredients": [],                                                                                           
    }     
    response = await client.put("/recipes/9999", json=payload)                                                         
    assert response.status_code == 404