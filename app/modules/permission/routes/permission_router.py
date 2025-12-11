from fastapi import APIRouter, Request
from app.modules.permission.middleware.permission_middleware import permission_required

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users")
@permission_required("view", group_id=1)
async def list_users(request: Request):
    return {"message": "User list, permission granted"}

@router.post("/users")
@permission_required("create", group_id=1)
async def create_user(request: Request):
    return {"message": "User created, permission granted"}
