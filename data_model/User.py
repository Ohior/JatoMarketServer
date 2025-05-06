from enum import Enum
from re import U
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from data_model.Developer import Developer

class UserType(Enum):
    TRADER = "trader"
    DEFAULT = "default"
    USER = "user"
    CUSTOMER = "customer"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    DEVELOPER = "developer"


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: str
    logitude:int = 0
    lattude:int = 0
    document_id: str | None = None
    store_document_uid: str | None = None
    meta_data: dict | None = None
    user_id: str|None = None
    is_active: bool = False
    user_type: UserType = UserType.DEFAULT
    developer: Developer | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at : str | None = None
    image_url: HttpUrl|None = None  # Accepts full URL to the image

    def update(self, **updates) -> "User":
        updated = self.model_dump()
        updated.update(updates)
        return User(**updated)
