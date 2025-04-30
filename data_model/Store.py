from beanie import Document
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from data_model.Product import Product
from data_model.User import User


class Store(BaseModel):
    store_name: str
    store_id:str
    user_id: str
    meta_data: dict | None = None
    products: List[Product] | None = None
    is_active: bool = False
    sales: float | None = None
    image_url: str | None = None  # Accepts full URL to the image
    updated_at : str | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    def update(self, **updates) -> "Store":
        updated = self.model_dump()
        updated.update(updates)
        return Product(**updated)
