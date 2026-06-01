from fastapi import APIRouter

hartley_violin_router = APIRouter(prefix="/api/hartley/violin", tags=["hartley-violin"])

@hartley_violin_router.get("/")
async def get_hartley_violin():
    pass