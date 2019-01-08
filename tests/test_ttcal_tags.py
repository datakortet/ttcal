# -*- coding: utf-8 -*-
from ttcal import Today, Year, Month, Day
from ttcal.templatetags.ttcal_tags import surround, chop_at_now, previous, is_current


def test_surround():
    t = Today()
    assert list(surround(t)) == [t-1, t]
    assert list(surround(t, '2')) == [t-2, t-1, t, t+1]


def test_chop_at_now():
    y = Year()
    m = Month()
    d = Day()
    assert chop_at_now([]) == []
    assert chop_at_now([y-1, y, y+1]) == [y-1, y]
    assert chop_at_now([m-1, m, m+1]) == [m-1, m]
    assert chop_at_now([d-1, d, d+1]) == [d-1, d]


def test_previous():
    t = Today()
    assert list(previous(t)) == [t-1]
    assert list(previous(t, '2')) == [t-1, t-2]


def test_is_current():
    assert is_current(Today())
    assert is_current(Month())
    assert is_current(Year())

    assert not is_current(Today() - 1)
    assert not is_current(Month() - 1)
    assert not is_current(Year() - 1)
