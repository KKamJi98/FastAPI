# TODO Review
import os
from fastapi import APIRouter, HTTPException, Depends
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.model.user import PrivateUser, PublicUser, SignInUser
from app.error import Duplicate, Missing


if os.getenv("CRYPTID_UNIT_TEST"):
    from app.fake import user as service
else:
    from app.service import user as service

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/user")

# --- 새로운 인증 관련 코드

# /user/token을 동작하게 함
# username과 password를 담고 있는 form을 읽음
# 접근 토큰 반환

oauth2_dep = OAuth2PasswordBearer(tokenUrl="/user/token")


def unauthed():
    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/token")
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """username과 password를 OAuth 양식에서 꺼내고 JWT 접근 토큰을 반환"""
    user = service.auth_user(name=form_data.username, plain=form_data.password)
    if not user:
        unauthed()
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(data={"sub": user.name}, expires=expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/token")
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    """현재 접근 토큰 반환"""
    return {"token": token}


# --- 이전 CRUD 코드


@router.get("/")
def get_all() -> list[PublicUser]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> PublicUser:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("/", status_code=201)
def create(user: SignInUser) -> PublicUser:
    try:
        return service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.patch("/{name}")
def modify(name: str, user: PrivateUser) -> PublicUser:
    try:
        return service.modify(name=name, user=user)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("/{name}")
def delete(name: str) -> None:
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)
