from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from data_model.Developer import Developer


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: str
    meta_data: dict | None = None
    user_id: str|None = None
    is_active: bool = False
    developer: Developer | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at : str | None = None
    image_url: HttpUrl|None = None  # Accepts full URL to the image

    def update(self, **updates) -> "User":
        updated = self.model_dump()
        updated.update(updates)
        return User(**updated)
