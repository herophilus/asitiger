from asitiger.secure import SecurePosition


def test_resolve_numeric():
    assert SecurePosition.resolve_value(123) == 123
    assert SecurePosition.resolve_value(0.5) == 0.5


def test_resolve_enum():
    assert (
        SecurePosition.resolve_value(SecurePosition.UNLOCKED)
        == SecurePosition.UNLOCKED.value
    )
