import os

# 데이터베이스를 메모리로 설정하는 환경 변수 설정
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"

import pytest
from app.model.creature import Creature
from app.service import creature as code
from app.error import Missing, Duplicate
from app.data import creature


# 샘플 데이터를 정의
@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="Yeti",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
        aka="Abominable Snowman",
    )


# 테스트 데이터 생성
def test_create(sample):
    resp = code.create(sample)
    assert resp == sample


# 데이터베이스에 삽입된 데이터를 가져오는 테스트
def test_get_exists(sample):
    resp = code.get_one(sample.name)
    assert resp == sample


# 존재하지 않는 데이터를 가져올 때 Missing 예외를 발생시키는지 테스트
def test_get_missing():
    with pytest.raises(Missing):
        code.get_one("boxturtle")
