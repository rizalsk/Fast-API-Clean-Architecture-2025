from pydantic import BaseModel

class BannerImageBase(BaseModel):
    file_path: str
    filename: str

class BannerImageResponse(BaseModel):
    id: int
    file_path: str
    filename: str

    class Config:
        from_attributes = True

class BannerImageCreate(BaseModel):
    file_path: str
    filename: str

    model_config = { "from_attributes": True }
