from asitiger.status import (
    AxisEnabledStatus,
    AxisStatus,
    JoystickStatus,
    LimitStatus,
    MotorStatus,
    RampingDirection,
    RampingStatus,
    Status,
    status_from_decimal,
    statuses_for_rdstat,
)

RDSTAT_RESPONSE = ":A  10N 138"


def test_status_from_decimal_types():
    axis = status_from_decimal(210)

    assert isinstance(axis.status, Status)
    assert isinstance(axis.enabled, AxisEnabledStatus)
    assert isinstance(axis.motor, MotorStatus)
    assert isinstance(axis.joystick, JoystickStatus)
    assert isinstance(axis.ramping, RampingStatus)
    assert isinstance(axis.ramping_direction, RampingDirection)
    assert isinstance(axis.upper_limit, LimitStatus)
    assert isinstance(axis.lower_limit, LimitStatus)


def test_status_from_decimal_values():
    axis = status_from_decimal(210)

    assert axis.status == Status.IDLE
    assert axis.enabled == AxisEnabledStatus.ENABLED
    assert axis.motor == MotorStatus.INACTIVE
    assert axis.joystick == JoystickStatus.DISABLED
    assert axis.ramping == RampingStatus.RAMPING
    assert axis.ramping_direction == RampingDirection.DOWN
    assert axis.upper_limit == LimitStatus.CLOSED
    assert axis.lower_limit == LimitStatus.CLOSED


def test_statuses_for_rdstat_split():
    axes = statuses_for_rdstat(RDSTAT_RESPONSE)

    assert len(axes) == 3


def test_statuses_for_rdstat_types():
    axes = statuses_for_rdstat(RDSTAT_RESPONSE)

    assert isinstance(axes[0], AxisStatus)
    assert isinstance(axes[1], Status)
    assert isinstance(axes[2], AxisStatus)


def test_from_flag_str():
    assert Status.from_flag("N") == Status.IDLE
    assert Status.from_flag("B") == Status.BUSY
