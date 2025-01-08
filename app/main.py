from fastapi import FastAPI, HTTPException
from fastapi_health import health
from elasticsearch_routes.elasticsearch_router import ElasticsearchRouter

def is_healthy():
    return {"database": "up", "cache": "up"}

app = FastAPI()
app.add_api_route("/health", health([is_healthy]))

app.include_router(ElasticsearchRouter)

@app.get("/")
def read_root():
    print("Hello FastAPI!")
    return {"message": "Hello FastAPI!"}
