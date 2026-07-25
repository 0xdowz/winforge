from winforge.core.tweak_loader import load_tier1_tweaks


def test_load_tier1_tweaks():
    tweaks = load_tier1_tweaks()
    assert len(tweaks) >= 15
    for t in tweaks:
        assert t.id != ""
        assert t.name != ""
        assert t.category is not None
