from typing import Union, List, Any
from fastapi import FastAPI
from api.routers import task
from pydantic import BaseModel

app = FastAPI()
# app.include_router(task.router)

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tags: List[str] = []

@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return Item