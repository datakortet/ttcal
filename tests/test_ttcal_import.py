# -*- coding: utf-8 -*-

"""Test that all modules are importable.
"""

import ttcal
import ttcal.calfns
import ttcal.day
import ttcal.duration
import ttcal.month
import ttcal.week
import ttcal.year


def test_import_():
    "Test that all modules are importable."
    
    assert ttcal
    assert ttcal.calfns
    assert ttcal.day
    assert ttcal.duration
    assert ttcal.month
    assert ttcal.week
    assert ttcal.year
