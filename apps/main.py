from fastapi import Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from titanic.app.james_controller import JamesController
from doro.app.doro_director import DoroDirector

app = FastAPI(title="WooJeongAlex Main Page")


class DatabaseHealthAdapter:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_connection(self) -> dict:
        try:
            result = await self.session.execute(text("SELECT NOW();"))
            now = result.scalar()
            return {"status": "success", "neon_time": now}
        except Exception as exc:
            return {"status": "error", "message": str(exc)}

@app.get("/")
def read_root():
    return {"message": "FAST API 메인 페이지", "docs": "/docs"}


@app.get("/db-check")
async def check_db(db: AsyncSession = Depends(get_db)):
    adapter = DatabaseHealthAdapter(db)
    return await adapter.check_connection()


@app.get("/titanic/data")
def read_titanic_data():
    james = JamesController()
    df = james.get_data()
    return df.to_dict(orient="records")

@app.get("/titanic/count")
def read_titanic_count():
    james = JamesController()
    count = james.get_count()
    return {"count": count}

@app.get("/titanic/count/survived")
def read_titanic_survived_count():
    james = JamesController()
    count = james.get_survived_count()
    return {"survived_count": count}

@app.get("/titanic/count/dead")
def read_titanic_dead_count():
    james = JamesController()
    count = james.get_dead_count()
    return {"dead_count": count}

@app.get("/titanic/tree")
def read_titanic_tree():
    james = JamesController()
    tree = james.has_decision_tree_model()

    return {"tree": tree}


@app.get("/titanic/model")
def read_titanic_model():
    controller = JamesController()
    model_name = controller.get_model_name_and_accuracy()
    return JSONResponse(content=jsonable_encoder(model_name))


@app.get("/doro/data")
def read_doro_data():
    doro_director = DoroDirector()
    df = doro_director.get_data()


    return df.to_dict(orient="records")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)