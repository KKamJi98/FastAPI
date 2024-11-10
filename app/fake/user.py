from app.model.user import SignInUser, PrivateUser, PublicUser
from app.error import Missing, Duplicate

fakes = [
    PublicUser(name="kwijobo"),
    PublicUser(name="ermagerd"),
]


def find(name: str) -> PublicUser | None:
    for user in fakes:
        if user.name == name:
            return user
    return None


def check_missing(name: str):
    if not find(name):
        raise Missing(msg=f"User {name} not found")


def check_duplicate(name: str):
    if find(name):
        raise Duplicate(msg=f"User {name} already exists")


def get_all() -> list[PublicUser]:
    """모든 유저 반환"""
    return fakes


def get_one(name: str) -> PublicUser:
    """name을 기반으로 특정 유저 반환"""
    check_missing(name)
    return find(name)


def create(user: PublicUser) -> PublicUser:
    """유저 생성"""
    check_duplicate(user.name)
    fakes.append(user)
    return user


def modify(name: str, user: PublicUser) -> PublicUser:
    """name으로 조회한 유저의 이름 수정"""
    check_missing(name)
    user0 = find(name)
    user0.name = user.name
    return user0


def delete(name: str) -> None:
    """name으로 조회한 유저 삭제"""
    check_missing(name)
    user = find(name)
    fakes.remove(user)
    return None
