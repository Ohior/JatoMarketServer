from beanie import Document
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from data_model.Product import Product
from data_model.User import User


class Store(BaseModel):
    store_name: str
    store_description: str
    store_id:str
    user_document_id: str
    logitude:float = 0.0
    lattude:float = 0.0
    document_id: str | None = None
    meta_data: dict | None = None
    products: List[Product] = []
    is_active: bool = False
    sales: int = 0
    image_url: str | None = None  # Accepts full URL to the image
    updated_at : str | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    def update(self, **updates) -> "Store":
        updated = self.model_dump()
        updated.update(updates)
        return Store(**updated)
