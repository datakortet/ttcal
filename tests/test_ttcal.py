import ttcal


def test_from_idtag():
    assert ttcal.from_idtag('m20124') == ttcal.Month(2012, 4)
