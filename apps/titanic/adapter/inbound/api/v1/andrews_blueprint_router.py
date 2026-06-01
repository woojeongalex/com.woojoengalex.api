from fastapi import APIRouter
andrews_blueprint_router = APIRouter(prefix="/api/andrews/blueprint", tags=["andrews-blueprint"])
@andrews_blueprint_router.get("/")
async def get_andrews_blueprint():
    pass