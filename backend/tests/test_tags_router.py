import pytest
                                                                                                                    
                                                                
@pytest.mark.asyncio                                                                                                 
async def test_get_tags_returns_empty_initially(client):        
    """空の DB で GET /tags/ が空配列を返すこと"""
    response = await client.get("/tags/")                                                                            
    assert response.status_code == 200
    assert response.json() == []                                                                                     
                                                                                                                    

@pytest.mark.asyncio                                                                                                 
async def test_post_tag_then_get_returns_one(client):           
    """POST /tags/ で1件作って、GET /tags/ で1件返ってくること"""                                                    
    # POST                                                                                                           
    create_resp = await client.post("/tags/", json={"title": "和食"})                                                
    assert create_resp.status_code == 200                                                                            
                                                                
    # GET                                                                                                            
    list_resp = await client.get("/tags/")                      
    assert list_resp.status_code == 200
    body = list_resp.json()
    assert len(body) == 1                                                                                            
    assert body[0]["title"] == "和食"
                                        