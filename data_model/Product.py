from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime


class Product(BaseModel):
    name: str
    store_id: str | None
    product_id: str | None = None
    meta_data: dict | None = None
    description: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: str | None = None
    price: float | None = None
    quantity: int | None = None
    image_url: HttpUrl | None = None

    def update(self, **updates) -> "Product":
        updated = self.model_dump()
        updated.update(updates)
        return Product(**updated)
