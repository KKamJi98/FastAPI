from docs.pydantic.model import Creature

dragon = Creature(
    name = "dragon",
    description=["incorrect", "string", "list"], # Error
    country="*",
    area="*",
    aka="firedrake",
)