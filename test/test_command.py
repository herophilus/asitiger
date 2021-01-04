from asitiger.command import Command


def test_format_coordinate_number():
    assert Command.format_coordinate("X", 12345.67) == "X=12345.67"


def test_format_coordinate_string():
    assert Command.format_coordinate("Y", "1") == "Y=1"


def test_format_coordinate_flag():
    assert Command.format_coordinate("Z", "1", flag_overrides=["+"]) == "Z=1"
    assert Command.format_coordinate("Z", "+", flag_overrides=["+"]) == "Z+"


def test_format_coordinate_flags():
    assert Command.format_coordinate("Z", "1", flag_overrides=["+", "-"]) == "Z=1"
    assert Command.format_coordinate("Z", "+", flag_overrides=["+", "-"]) == "Z+"


def test_format_coorindate_truncation():
    assert (
        Command.format_coordinate("W", "-123456789.123456789") == "W=-123456789.12345"
    )


def test_format_coordinates():
    assert Command.format_coordinates({"X": 1, "Y": "2", "Z": 3.0}) == "X=1 Y=2 Z=3.0"


def test_format_coordinates_flags():
    assert (
        Command.format_coordinates(
            {"X": "+", "Y": "?", "Z": "!"}, flag_overrides=["+", "?"]
        )
        == "X+ Y? Z=!"
    )


def test_format_with_coords():
    assert Command.format("CMD", {"X": 1, "Y": -2.0}) == "CMD X=1 Y=-2.0"


def test_format_empty_coords():
    assert Command.format("CMD", {}) == "CMD"


def test_format_card_address():
    assert Command.format("CMD", {}, card_address=123) == "123CMD"
