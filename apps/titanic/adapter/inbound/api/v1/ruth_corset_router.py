from fastapi import APIRouter

ruth_corset_router = APIRouter(prefix="/api/ruth/corset", tags=["ruth-corset"])

@ruth_corset_router.get("/")
async def get_ruth_corset():
    pass