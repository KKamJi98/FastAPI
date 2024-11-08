from .init import curs, conn
from app.model.explorer import Explorer

def row_to_model(row: tuple) -> Explorer:
    return Explorer(name=row[0], country=row[1], description=row[2])


def model_to_dict(explorer: Explorer) -> dict:
    return explorer.model_dump() if explorer else None


def get_one(name: str) -> Explorer:
    query = "select * from explorer where name = :name"
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    return row_to_model(row)


def get_all() -> list[Explorer]:
    query = "select * from explorer"
    curs.execute(query)
    return [row_to_model(row) for row in curs.fetchall()]


def create(explorer: Explorer) -> Explorer:
    query = """insert into explorer (name, country, description)
                values (:name, :country, :description)"""
    params = model_to_dict(explorer)
    curs.execute(query, params)
    conn.commit()
    return get_one(explorer.name)

def modify(name: str, explorer: Explorer) -> Explorer:
    query = """update explorer
                set country = :country, 
                description = :description
                where name = :name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = explorer.name
    curs.execute(query, params)
    conn.commit()
    return get_one(explorer.name)

def delete(explorer: Explorer) -> bool:
    query = "delete from explorer where name = :name"
    params = {"name": explorer.name}
    res = curs.execute(query, params)
    conn.commit()
    return bool(res)
