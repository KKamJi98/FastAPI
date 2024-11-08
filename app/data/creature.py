from .init import curs, conn
from app.model.creature import Creature

def row_to_model(row: tuple) -> Creature:
    """fetch함수가 반환한 튜플을 모델 객체로 변환"""
    (name, description, country, area, aka) = row
    return Creature(name, description, country, area, aka)


def model_to_dict(creature: Creature) -> dict:
    """Pydantic 모델을 딕셔너리로 변환해 쿼리 매개변수로 알맞게 지정"""
    return creature.model_dump()


def get_one(name: str) -> Creature:
    query = "select * from creature where name =:name"
    params = {"name": name}
    curs.execute(query, params)
    return row_to_model(curs.fetchone())

def get_all(name: str) -> list[Creature]:
    query = "select * from creature"
    curs.execute(query)
    return [row_to_model(row) for row in curs.fetchall()]

def create(creature: Creature) -> Creature:
    query = """insert into creature values
            (:name, :description, :country, :area, :aka)"""
    params = model_to_dict(creature)
    curs.execute(query, params)
    conn.commit()
    return get_one(creature.name)


def modify(creature: Creature) -> Creature:
    query = """update creature 
                set country=:country,
                    name=:name,
                    description = :description,
                    area = :area,
                    aka = :aka
                where name = :name_orig"""
    params = model_to_dict(creature)
    params["name_orig"] = creature.name
    curs.execute(query, params)
    conn.commit()
    return get_one(creature.name)

def delete(creature: Creature) -> bool:
    query = "delete from creature where name = :name"
    params = {"name": creature.name}
    res = curs.execute(query, params)
    conn.commit()
    return bool(res)
