from winforge.core.checksums import verify_tweak_checksums


def test_verify_tweak_checksums():
    valid, warnings = verify_tweak_checksums()
    assert isinstance(valid, bool)
    assert isinstance(warnings, list)
