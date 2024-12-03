import os
os.environ["UNIT_TEST"] = "true"

import test.unit.mock.mod2 as mod2

def test_summer_fake():
    assert "The sum is 11" == mod2.summer(5, 6)

