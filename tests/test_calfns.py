# -*- coding: utf-8 -*-
from ttcal.calfns import rangecmp


def test_rangecmp():
    assert rangecmp((1, 1), (1, 1)) == 0   # identical
    assert rangecmp((3, 4), (1, 1)) == 1   # (3,4)>(1,1)
    assert rangecmp((1, 4), (3, 5)) == 0   # overlap
    assert rangecmp((1, 5), (3, 4)) == 0   # (3,4) contained in (1,5)
    assert rangecmp((1, 2), (2, 4)) == -1  # (1,2) less than and doesn't overlap (2,4)
    assert rangecmp((3, 4), (1, 5)) == 0   # (3,4) contained in (1,5)
