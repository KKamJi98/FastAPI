from unittest import mock
import test.unit.mock.mod1 as mod1
import test.unit.mock.mod2 as mod2

def test_caller_a():
    with mock.patch("test.unit.mock.mod1.preamble", return_value=""):
        assert "11" == mod2.summer(5, 6)
        
def test_caller_b():
    with mock.patch("test.unit.mock.mod1.preamble") as mock_preamble:
        mock_preamble.return_value = ""
        assert "11" == mod2.summer(5, 6)

@mock.patch("test.unit.mock.mod1.preamble", return_value="")
def test_caller_c(mock_preamble):
    assert "11" == mod2.summer(5, 6)

@mock.patch("test.unit.mock.mod1.preamble")
def test_caller_d(mock_preamble):
    mock_preamble.return_value = ""
    assert "11" == mod2.summer(5, 6)