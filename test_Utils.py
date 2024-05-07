import pytest
from datetime import datetime
from Utils import parse_line, ConvertToEuro  # replace 'your_module' with the actual module name

def test_parse_line():
    line = "[03.05.2024 17:37:37] Payed $15.0 to Titan ┃ RTLploppey"
    expected_result = {
        "timestamp": datetime.strptime("03.05.2024 17:37:37", "%d.%m.%Y %H:%M:%S"),
        "action": "Payed",
        "amount": "15.0",
        "player": "RTLploppey",
    }
    assert parse_line(line) == expected_result

    line = "[03.05.2024 17:37:37] Received $154.05 from Titan ┃ RTLploppey"
    expected_result = {
        "timestamp": datetime.strptime("03.05.2024 17:37:37", "%d.%m.%Y %H:%M:%S"),
        "action": "Received",
        "amount": "154.05",
        "player": "RTLploppey",
    }
    assert parse_line(line) == expected_result

def test_ConvertToEuro():
    assert ConvertToEuro("1000000") == 5.0
    assert ConvertToEuro("5000000") == 25.0
    assert ConvertToEuro("0") == 0.0

    with pytest.raises(ValueError):  # test if non-numeric input raises an error
        ConvertToEuro("not a number")