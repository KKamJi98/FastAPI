from docs.pydantic.model import Creature
from fastapi import FastAPI

app = FastAPI()


@app.get("/creature")
def get_all() -> list[Creature]:
    from docs.pydantic.data import get_creatures

    return get_creatures()
