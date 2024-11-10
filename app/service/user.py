# TODO Review
from datetime import timedelta, datetime
import os
from jose import jwt
import bcrypt
from app.model.user import PublicUser, PrivateUser, SignInUser

if os.getenv("CRYPTID_UNIT_TEST"):
    from app.fake import user as data
else:
    from app.data import user as data


# --- 새로운 인증 관련 코드

# SECRET_KEY는 반드시 바꾸고 배포해야 함
SECRET_KEY = "keep-it-secret-keep-it-safe"
ALGORITHM = "HS256"


def verify_password(plain: str, hash: str) -> bool:
    """plain의 hash 값과, 데이터베이스의 hash 값과 비교"""
    password_bytes = plain.encode("utf-8")
    hash_bytes = hash.encode("utf-8")
    return bcrypt.checkpw(password=password_bytes, hashed_password=hash_bytes)


def get_hash(plain: str) -> str:
    """plain의 hash 값 반환"""
    password_bytes = plain.encode("utf-8")
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(password_bytes, salt)
    return hash_bytes.decode("utf-8")


def get_jwt_username(token: str) -> str | None:
    """JWT 접근 토큰으로부터 username을 반환"""
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        if not (username := payload.get("sub")):
            return None
    except jwt.JWTError:
        return None
    return username


def get_current_user(token: str) -> PublicUser | None:
    """OAuth 토큰을 풀어 PublicUser를 반환"""
    if not (username := get_jwt_username(token)):
        return None
    if user := lookup_user(username=username):
        return user
    return None


def lookup_user(username: str, is_public=True) -> PublicUser | PrivateUser | None:
    """
    데이터베이스에서 username에 매칭되는 User 반환
    is_public이 True이면 PublicUser를 반환하고, False이면 PrivateUser를 반환
    hash 속성은 PrivateUser만 가지고 있음. 비밀번호 인증을 위해 hash 속성이 필요
    """
    if user := data.get_one(username, is_public):
        return user
    return None


def auth_user(name: str, plain: str) -> PublicUser | PrivateUser | None:
    """name과 plain 암호로 유저를 인증"""
    if not (user := lookup_user(username=name, is_public=False)):
        return None
    if not verify_password(plain=plain, hash=user.hash):
        return None
    return user


def create_access_token(data: dict, expires: timedelta | None = None):
    """JWT 접근 토큰을 반환"""
    src = data.copy()
    now = datetime.utcnow()
    if not expires:
        expires = timedelta(minutes=15)
    src.update({"exp": now + expires})
    encoded_jwt = jwt.encode(claims=src, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- CRUD 통과 코드


def get_all() -> list[PublicUser]:
    """모든 유저 반환"""
    return data.get_all()


def get_one(name) -> PublicUser:
    """name을 기반으로 특정 유저 반환"""
    return data.get_one(name)


# data.create는 hash 속성을 지닌 PrivateUser가 필요
# SignInUser의 password를 해시한 hash 속성을 가지고 있는 PrivateUser를 만들어서 전달
def create(sign_in_user: SignInUser) -> PublicUser:
    """새로운 유저 생성"""
    user = PrivateUser(name=sign_in_user.name, hash=get_hash(sign_in_user.password))
    return data.create(user)


def modify(name: str, user: PublicUser) -> PublicUser:
    """name을 기반으로 특정 유저 수정"""
    return data.modify(name=name, user=user)


def delete(name: str) -> None:
    return data.delete(name=name)
