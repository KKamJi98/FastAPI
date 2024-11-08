from app.model.explorer import Explorer

_explorers = [
    Explorer(
        name="Claude Hande", country="FR", description="보름달이 뜨면 만나기 힘듦"
    ),
    Explorer(
        name="Noah Weiser", country="DE", description="눈이 나쁘고 벌목도를 가지고 다님"
    ),
]


def get_all() -> list[Explorer]:
    """Get all explorers"""
    return _explorers


def get_one(name: str) -> Explorer:
    """Get a single explorer"""
    for _explorer in _explorers:
        if _explorer.name == name:
            return _explorer
    return None


def create(explorer: Explorer) -> Explorer:
    """Create a new explorer"""
    _explorers.append(explorer)
    return explorer


def modify(name: str, explorer: Explorer) -> Explorer:
    """Modify an existing explorer"""
    for index, _explorer in enumerate(_explorers):
        if _explorer.name == name:
            _explorers[index] = explorer
            return explorer
    return None


def replace(name: str, explorer: Explorer) -> Explorer:
    """Replace an existing explorer"""
    for index, _explorer in enumerate(_explorers):
        if _explorer.name == name:
            _explorers[index] = explorer
            return explorer
    return None


def delete(name: str) -> bool:
    """Delete an existing explorer"""
    for index, _explorer in enumerate(_explorers):
        if _explorer.name == name:
            _explorers.pop(index)
            return True
    return False
