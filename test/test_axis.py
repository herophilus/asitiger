import pytest

from asitiger.axis import Axis


@pytest.fixture()
def build_info():
    return [
        "TIGER_COMM",
        "Motor Axes: X Z S O L",
        "Axis Types: x z f o i",
        "Axis Addr: 1 2 2 3 7",
        "Hex Addr: 31 32 32 33 37",
        "Axis Props:  74   2   2   0   0",
        "SOME_EXTRA STUFF",
        "DOWN_HERE",
    ]


def test_num_axes(build_info):
    assert len(Axis.get_axes_from_build(build_info)) == 5


def test_axis_labels(build_info):
    axes = Axis.get_axes_from_build(build_info)
    assert list(map(lambda axis: axis.label, axes)) == ["X", "Z", "S", "O", "L"]


def test_axis_types(build_info):
    axes = Axis.get_axes_from_build(build_info)
    assert list(map(lambda axis: axis.type, axes)) == [
        Axis.Type.XY_MOTOR,
        Axis.Type.Z_MOTOR,
        Axis.Type.SLIDER,
        Axis.Type.TURRET,
        Axis.Type.MULTI_LED,
    ]


def test_axis_addresses(build_info):
    axes = Axis.get_axes_from_build(build_info)
    assert list(map(lambda axis: axis.address, axes)) == [
        "1",
        "2",
        "2",
        "3",
        "7",
    ]


def test_axis_hex_addresses(build_info):
    axes = Axis.get_axes_from_build(build_info)
    assert list(map(lambda axis: axis.address_hex, axes)) == [
        "31",
        "32",
        "32",
        "33",
        "37",
    ]
