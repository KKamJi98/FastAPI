# TODO Review
from .init import curs, conn, IntegrityError
from app.model.explorer import Explorer
from app.error import Missing, Duplicate


curs.execute(
    """CREATE TABLE IF NOT EXISTS explorer (
            name TEXT PRIMARY KEY,
            country TEXT,
            description TEXT
        )"""
)


def row_to_model(row: tuple) -> Explorer:
    return Explorer(name=row[0], country=row[1], description=row[2])


def model_to_dict(explorer: Explorer) -> dict:
    return explorer.model_dump() if explorer else None


def get_one(name: str) -> Explorer:
    query = "select * from explorer where name = :name"
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Explorer {name} not found")


def get_all() -> list[Explorer]:
    query = "select * from explorer"
    curs.execute(query)
    return [row_to_model(row) for row in curs.fetchall()]


def create(explorer: Explorer) -> Explorer:
    if not explorer:
        return None
    query = """insert into explorer (name, country, description)
                values (:name, :country, :description)"""
    params = model_to_dict(explorer)
    try:
        curs.execute(query, params)
    except IntegrityError:
        raise Duplicate(msg=f"Explorer {explorer.name} already exists")
    conn.commit()
    return get_one(explorer.name)


def replace(name: str, explorer: Explorer) -> Explorer:
    if not (name and explorer):
        return None
    query = """update explorer
                set name = :name,
                    country = :country,
                    description = :description
                where name = :name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = name
    curs.execute(query, params)
    if curs.rowcount == "1":
        conn.commit()
        return get_one(explorer.name)
    else:
        raise Missing(msg=f"Explorer {name} not found")


def modify(name: str, explorer: Explorer) -> Explorer:
    if not (name and explorer):
        return None
    query = """update explorer
                set country = :country, 
                description = :description
                where name = :name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = name
    curs.execute(query, params)
    if curs.rowcount == "1":
        conn.commit()
        return get_one(explorer.name)
    else:
        raise Missing(msg=f"Explorer {name} not found")


def delete(name: str):
    if not name:
        return False
    query = "delete from explorer where name = :name"
    params = {"name": name}
    curs.execute(query, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Explorer {name} not found")
    conn.commit()
