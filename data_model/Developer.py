from pydantic import BaseModel, HttpUrl


class Developer(BaseModel):
    secret_api_key: str | None = None
    publick_api_key: str | None = None
    url: HttpUrl | None = None
    meta_data: dict | None = None

