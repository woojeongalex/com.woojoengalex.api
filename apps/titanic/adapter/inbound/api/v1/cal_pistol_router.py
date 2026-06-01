from fastapi import APIRouter

cal_pistol_router = APIRouter(prefix="/api/cal/pistol", tags=["cal-pistol"])

@cal_pistol_router.get("/")
async def get_cal_pistol():
    pass
