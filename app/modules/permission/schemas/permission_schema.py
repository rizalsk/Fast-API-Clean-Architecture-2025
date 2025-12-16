from pydantic import BaseModel

class PermissionSchema(BaseModel):
    id: int
    name: str
    is_default: bool

    class Config:
        from_attributes = True