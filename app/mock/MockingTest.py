from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
client = TestClient(app)

# 의존성 함수
def get_db():
    return {"db": "real_database"}

@app.get("/items/")
def read_items(db=Depends(get_db)):
    return db

# 테스트용 Mock DB
def override_get_db():
    return {"db": "mock_database"}

app.dependency_overrides[get_db] = override_get_db

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {"db": "mock_database"}