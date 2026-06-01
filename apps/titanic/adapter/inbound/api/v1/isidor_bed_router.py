from fastapi import APIRouter

isidor_bed_router = APIRouter(prefix="/api/isidor/bed", tags=["isidor-bed"])

@isidor_bed_router.get("/")
async def get_isidor_bed():
    pass