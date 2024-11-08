from app.model.creature import Creature

_creatures = [
    Creature(
        name="Yeti",
        aka="Abominable Snowman",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
    ),
    Creature(
        name="Sasquatch",
        aka="The Scream",
        country="US",
        area="*All*",
        description="Yeti's cousin",
    ),
    Creature(
        name="Bigfoot",
        aka="Sasquatch",
        country="US",
        area="*All*",
        description="Yeti's cousin",
    ),
]


def get_all() -> list[Creature]:
    """Get all creatures"""
    return _creatures


def get_one(name: str) -> Creature | None:
    """Get a single creature"""
    for _creature in _creatures:
        if _creature.name == name:
            return _creature
    return None


def create(creature: Creature) -> Creature:
    """Create a new creature"""
    _creatures.append(creature)
    return creature


def modify(name: str, creature: Creature) -> Creature | None:
    """Modify an existing creature"""
    for index, _creature in enumerate(_creatures):
        if _creature.name == name:
            _creatures[index] = creature
            return _creature
    return None


def replace(name: str, creature: Creature) -> Creature | None:
    """Replace an existing creature"""
    for index, _creature in enumerate(_creatures):
        if _creature.name == name:
            _creatures[index] = creature
            return _creature
    return None


def delete(name: str) -> bool:
    """Delete an existing creature"""
    for index, _creature in enumerate(_creatures):
        if _creature.name == name:
            _creatures.pop(index)
            return True
    return False
