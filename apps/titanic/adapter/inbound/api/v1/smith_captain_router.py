from fastapi import APIRouter

smith_captain_router = APIRouter(prefix="/api/smith/captain", tags=["smith-captain"])

@smith_captain_router.get("/")
async def get_smith_captain():
    pass