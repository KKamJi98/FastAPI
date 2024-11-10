# TODO Review
from app.model.user import PublicUser, PrivateUser, SignInUser
from .init import conn, curs, get_db, IntegrityError
from app.error import Missing, Duplicate


"""
user(활성 유저), xuser(삭제된 유저)를 분리해 삭제된 유저의 데이터를 다른 테이블로 옮겨 쿼리 속도 향상
- boolean 필드 최소화
- 테이블 크기 최적화
"""
curs.execute(
    """create table if not exists
                    user(
                        name text primary key,
                        hash text)"""
)
curs.execute(
    """create table if not exists
                    xuser(
                        name text primary key,
                        hash text)"""
)


# is_public 인자에 따라 나가는 모델이 분기됨
def row_to_model(row: tuple, is_public: bool = True) -> PublicUser | PrivateUser:
    name, hash = row
    if is_public:
        return PublicUser(name=name)
    else:
        return PrivateUser(name=name, hash=hash)


def model_to_dict(user: PrivateUser) -> dict:
    return user.model_dump()


# is_public 인자에 따라 PublicUser 또는 PrivateUser 반환
def get_one(name: str, is_public: bool = True) -> PublicUser | PrivateUser:
    query = "select * from user where name=:name"
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row, is_public=is_public)
    else:
        raise Missing(msg=f"User {name} not found")


# 유저 목록 조회에서는 hash를 포함할 일이 없어 PublicUser 모델 집합을 반환
def get_all() -> list[PublicUser]:
    query = "select * from user"
    curs.execute(query)
    return [row_to_model(row) for row in curs.fetchall()]


# 유저 생성을 위해 password를 암호화한 hash 값을 저장해야 함
# create 함수는 user 인자가 hash 값을 가지고 있는 것으로 간주
# 저장이 완료되면 외부로 노출돼도 되는 PublicUser를 반환
def create(user: PrivateUser, table: str = "user") -> PublicUser:
    """user 테이블 또는 xuser 테이블에 유저를 생성"""
    query = f"""insert into {table}
                (name, hash)
                values 
                (:name, :hash)"""
    params = model_to_dict(user)
    try:
        curs.execute(query, params)
    except IntegrityError:
        raise Duplicate(msg=f"{table}: user {user.name} already exists")
    return PublicUser(name=user.name)


# name만 외부로 노출되므로 name에 대한 변경만 가능
def modify(name: str, user: PublicUser) -> PublicUser:
    """name으로 조회한 유저의 이름 수정"""
    query = """update user set
                name=:name
                where name=:name0"""
    params = {"name": user.name, "name0": name}

    curs.execute(query, params)
    if curs.rowcount == 1:
        return get_one(user.name)
    else:
        raise Missing(msg=f"User {name} not found")


def delete(name: str) -> None:
    """name을 기반으로 user 테이블에서 유저를 삭제하고, xuser 테이블에 추가"""
    user = get_one(name, is_public=False)
    query = "delete from user where name = :name"
    params = {"name": name}
    curs.execute(query, params)
    if curs.rowcount == 1:
        create(user, table="xuser")
    else:
        raise Missing(msg=f"User {name} not found")
