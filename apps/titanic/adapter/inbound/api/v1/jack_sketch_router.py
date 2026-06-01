from fastapi import APIRouter

jack_sketch_router = APIRouter(prefix="/api/jack/sketch", tags=["jack-sketch"])

@jack_sketch_router.get("/")
async def get_jack_sketch():
    pass