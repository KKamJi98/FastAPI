import os

if os.getenv("UNIT_TEST"):
    import test.unit.mock.fake_mod1 as mod1
else:
    import test.unit.mock.mod1 as mod1
    
def summer(x: int, y: int) -> str:
    return mod1.preamble() + f"{x+y}"