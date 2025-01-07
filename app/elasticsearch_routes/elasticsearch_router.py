from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from elasticsearch import Elasticsearch

ElasticsearchRouter = APIRouter()

# Elasticsearch 클라이언트 초기화
es = Elasticsearch("http://host.docker.internal:9200")

INDEX_NAME = "items"

class Item(BaseModel):
    item_id: int
    name: str
    description: str

@ElasticsearchRouter.post("/items/")
def create_item(item: Item):
    item_id = item.item_id
    name = item.name
    description = item.description
    print(f"Creating item {item_id} with name {name} and description {description}")
    if es.exists(index=INDEX_NAME, id=item_id):
        raise HTTPException(status_code=400, detail="Item already exists")
    
    document = {
        "name": name,
        "description": description,
    }
    es.index(index=INDEX_NAME, id=item_id, document=document)
    return {"message": "Item created", "item": document}

@ElasticsearchRouter.get("/items/{item_id}")
def read_item(item_id: int):
    if not es.exists(index=INDEX_NAME, id=item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    
    item = es.get(index=INDEX_NAME, id=item_id)
    return item["_source"]

@ElasticsearchRouter.put("/items/{item_id}")
def update_item(item_id: int, name: str = None, description: str = None):
    if not es.exists(index=INDEX_NAME, id=item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    
    document = es.get(index=INDEX_NAME, id=item_id)["_source"]
    if name:
        document["name"] = name
    if description:
        document["description"] = description

    es.index(index=INDEX_NAME, id=item_id, document=document)
    return {"message": "Item updated", "item": document}

@ElasticsearchRouter.delete("/items/{item_id}")
def delete_item(item_id: int):
    if not es.exists(index=INDEX_NAME, id=item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    
    es.delete(index=INDEX_NAME, id=item_id)
    return {"message": "Item deleted"}
