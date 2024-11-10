# Review Complete (1)
from .init import curs, conn, IntegrityError
from app.model.creature import Creature
from app.error import Missing, Duplicate

curs.execute(
    """CREATE TABLE IF NOT EXISTS creature (
            name TEXT PRIMARY KEY,
            description TEXT,
            country TEXT,
            area TEXT,
            aka TEXT
        )"""
)


def row_to_model(row: tuple) -> Creature:
    """fetch함수가 반환한 튜플을 모델 객체로 변환"""
    (name, description, country, area, aka) = row
    return Creature(
        name=name, description=description, country=country, area=area, aka=aka
    )


def model_to_dict(creature: Creature) -> dict:
    """Pydantic 모델을 딕셔너리로 변환해 쿼리 매개변수로 알맞게 지정"""
    print(creature.model_dump())
    return creature.model_dump() if creature else None


def create(creature: Creature) -> Creature:
    query = """insert into creature values
            (:name, :description, :country, :area, :aka)"""
    params = model_to_dict(creature)
    try:
        curs.execute(query, params)
    except IntegrityError:
        raise Duplicate(msg=f"Creature {creature.name} already exists")
    conn.commit()
    return get_one(creature.name)


def get_one(name: str) -> Creature:
    query = "select * from creature where name =:name"
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Creature {name} not found")


def get_all() -> list[Creature]:
    query = "select * from creature"
    curs.execute(query)
    return [row_to_model(row) for row in curs.fetchall()]


def replace(name: str, creature: Creature) -> Creature:
    if not (name and creature):
        return None

    # 대상 행이 존재하는지 확인
    try:
        get_one(name)
    except Missing:
        raise Missing(msg=f"Creature {name} not found")

    try:
        # 기존 행 삭제
        delete_query = "DELETE FROM creature WHERE name = :name_orig"
        delete_params = {"name_orig": name}
        curs.execute(delete_query, delete_params)

        # 새로운 행 삽입
        insert_query = """INSERT INTO creature (name, description, country, area, aka)
                            VALUES (:name, :description, :country, :area, :aka)"""
        params = model_to_dict(creature)
        curs.execute(insert_query, params)

        # 커밋
        conn.commit()
    except IntegrityError:
        conn.rollback()
        raise Duplicate(msg=f"Creature {creature.name} already exists")
    except Exception as e:
        conn.rollback()
        raise e

    return get_one(creature.name)


def modify(name: str, creature: Creature) -> Creature:
    if not (name and creature):
        return None
    query = """update creature 
                set country=:country,
                    name=:name,
                    description = :description,
                    area = :area,
                    aka = :aka
                where name = :name_orig"""
    params = model_to_dict(creature)
    params["name_orig"] = name  # 수정 전의 이름 사용
    curs.execute(query, params)
    if curs.rowcount:
        conn.commit()
        return get_one(creature.name)
    else:
        raise Missing(msg=f"Creature {name} not found")


def delete(name: str):
    if not name:
        return False
    query = "delete from creature where name = :name"
    params = {"name": name}
    curs.execute(query, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Creature {name} not found")
    conn.commit()
