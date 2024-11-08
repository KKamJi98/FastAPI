from fastapi import APIRouter
from app.model.creature import Creature
import app.service.creature as service

router = APIRouter(prefix="/creature")


@router.get("")
@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Creature | None:
    return service.get_one(name)


@router.post("")
@router.post("/")
def create(creature: Creature) -> Creature:
    return service.create(creature)


@router.patch("/{name}")
def modify(name: str, creature: Creature) -> Creature | None:
    return service.modify(name, creature)


@router.put("/{name}")
def replace(name, creature: Creature) -> Creature | None:
    return service.replace(name, creature)


@router.delete("/{name}")
def delete(name: str):
    return service.delete(name)
