# -*- coding: utf-8 -*-

"""Test that all modules are importable.
"""

import ttcal.calfns
import ttcal.day
import ttcal.duration
import ttcal.month
import ttcal.templatetags
import ttcal.templatetags.ttcal_tags
import ttcal.week
import ttcal.year


def test_import_():
    "Test that all modules are importable."
    
    assert ttcal.calfns
    assert ttcal.day
    assert ttcal.duration
    assert ttcal.month
    assert ttcal.templatetags
    assert ttcal.templatetags.ttcal_tags
    assert ttcal.week
    assert ttcal.year
