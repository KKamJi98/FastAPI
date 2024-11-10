# Review Complete (1)
import os
import pytest
from app.model.creature import Creature
from app.error import Missing, Duplicate


# data.init에 메모리 DB를 사용하도록 data 모듈을 가져오기 전에 설정
# ":memory: 옵션을 사용하면 데이터베이스가 메모리 내에서만 생성되어 실행됨"
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"

from app.data import creature


# Fixture => 테스트 환경에서 공통으로 사용되는 객체나 리소스를 생성하고 초기화하는 기능을 제공
@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="yeti",
        country="CN",
        area="Himalayas",
        description="Harmless Himalayan",
        aka="Abominable Snowman",
    )


@pytest.fixture
def wrong_sample() -> Creature:
    return Creature(
        name="phoenix",
        country="EG",
        area="Mythical Lands",
        description="Legendary immortal bird",
        aka="Firebird",
    )


def test_create(sample):
    resp = creature.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        creature.create(sample)


def test_get_one(sample):
    resp = creature.get_one(sample.name)
    assert resp == sample


def test_get_one_missing(wrong_sample):
    with pytest.raises(Missing):
        _ = creature.get_one(wrong_sample.name)


def test_replace(sample):
    sample.description = "Updated Description"
    sample.area = "Updated Area"

    resp = creature.replace(sample.name, sample)

    assert resp == sample

    retrieved = creature.get_one(sample.name)
    assert retrieved == sample


def test_replace_missing(wrong_sample):
    with pytest.raises(Missing):
        _ = creature.replace(wrong_sample.name, wrong_sample)


def test_modify(sample):
    sample.area = "Sesame Street"
    resp = creature.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing(wrong_sample):
    with pytest.raises(Missing):
        _ = creature.modify(wrong_sample.name, wrong_sample)


def test_delete(sample):
    resp = creature.delete(sample.name)
    assert resp is None


def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = creature.delete(sample.name)
