# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from unittest import TestCase
import ttcal
import pytest

try:
    unicode
except NameError:
    unicode = str


@pytest.fixture
def dd():
    return [
        ttcal.Duration(days=1, hours=3, minutes=14, seconds=20),
        ttcal.Duration(days=0, hours=1, minutes=10, seconds=0),
        ttcal.Duration(days=0, hours=0, minutes=70, seconds=0),
        ttcal.Duration(timedelta(minutes=70)),
    ]


@pytest.fixture
def toint_obj():
    class Foo(object):
        def toint(self):
            return 42
    return Foo()


def test_sum(dd):
    assert ttcal.Duration.sum(dd) == ttcal.Duration(days=1, hours=6, minutes=44, seconds=20)


def test_duration_tuple(dd):
    assert dd[0].duration_tuple() == ('', 27, 14, 20)


def test_str(dd):
    assert str(dd[1]) == '1:10:00'
    assert str(dd[2]) == '1:10:00'
    assert "%s" % dd[3] == '1:10:00'
    assert unicode(dd[1]) == u'1:10:00'


def test_eq(dd):
    assert dd[1] == timedelta(hours=1, minutes=10)
    assert timedelta(hours=1, minutes=10) == dd[1]
    assert ttcal.Duration() == 0
    assert 0 == ttcal.Duration()
    assert dd[1] - dd[1] == 0
    assert 0 == dd[1] - dd[1]
    assert not (dd[0] == "foo")


def test_duration_rmeth():
    class Foo(object):
        def __req__(self, other):
            return 42

        def __rne__(self, other):
            return 43

        def __rlt__(self, other):
            return 44

        def __rgt__(self, other):
            return 45

        def __rle__(self, other):
            return 46

        def __rge__(self, other):
            return 47

    assert (ttcal.Duration(years=2) == Foo()) == 42
    assert (ttcal.Duration(years=2) != Foo()) == 43
    assert (ttcal.Duration(years=2) < Foo()) == 44
    assert (ttcal.Duration(years=2) > Foo()) == 45
    assert (ttcal.Duration(years=2) <= Foo()) == 46
    assert (ttcal.Duration(years=2) >= Foo()) == 47


def test_ne(dd):
    assert dd[0] != dd[1]
    assert dd[1] != timedelta(hours=2)
    assert dd[1] != 0
    assert not (dd[1] != 'foo')


def test_lt(dd, toint_obj):
    assert dd[1] < dd[0]
    assert dd[1] <= dd[0]
    assert not (dd[1] < 'Foo')
    assert not (dd[1] <= 'Foo')
    assert not dd[0] < toint_obj
    assert not dd[0] <= toint_obj


def test_gt(dd, toint_obj):
    assert dd[0] > dd[1]
    assert dd[0] >= dd[1]
    assert not (dd[1] > 'Foo')
    assert not (dd[1] >= 'foo')
    assert dd[1] > 1
    assert dd[0] > toint_obj
    assert dd[0] >= toint_obj


def test_repr(dd):
    assert repr(dd[1]) == 'Duration(hours=1, minutes=10, seconds=0)'


def test_accessors(dd):
    assert dd[0].hrs == 27
    assert dd[0].mins == 14
    assert dd[0].secs == 20


def test_parse(dd):
    assert dd[1].parse('01:10:00') == dd[2]
    assert ttcal.Duration.parse("") is None
    assert ttcal.Duration.parse("-1:10") == ttcal.Duration(hours=-1, minutes=-10)


def test_add(dd):
    assert dd[2] + dd[3] == ttcal.Duration(hours=2, minutes=20)


def test_sub(dd):
    tmp = ttcal.Duration(days=1, hours=2, minutes=4, seconds=20)
    assert dd[0] - dd[1] == tmp


def test_mul(dd):
    assert dd[2] * 3 == ttcal.Duration(hours=3, minutes=30)


def test_div(dd):
    assert dd[2] / 2 == ttcal.Duration(minutes=35)
    assert dd[2] // 2 == ttcal.Duration(minutes=35)
    # there are 4 x 15mins in 1 hour..
    assert ttcal.Duration(hours=1) / ttcal.Duration(minutes=15) == 4.0
    # assert ttcal.Duration(hours=1) // ttcal.Duration(minutes=15) == 4
    # we don't raise zero division errors.
    assert ttcal.Duration(hours=1) / ttcal.Duration() == 0.0
    # assert ttcal.Duration(hours=1) // ttcal.Duration() == 0
