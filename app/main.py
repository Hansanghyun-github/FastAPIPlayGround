from fastapi import FastAPI, HTTPException
from elasticsearch_routes.elasticsearch_router import ElasticsearchRouter

app = FastAPI()

app.include_router(ElasticsearchRouter)

@app.get("/")
def read_root():
    print("Hello FastAPI!")
    return {"message": "Hello FastAPI!"}
