# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from unittest import TestCase
import ttcal
import pytest
from ttcal import Day


@pytest.fixture
def week():
    return [
        ttcal.Week.weeknum(4, 2012),
        ttcal.Week.weeknum(1),
        ttcal.Week.weeknum(52, 2012),
        ttcal.Week.weeknum(4, 2012),
    ]


def test_range(week):
    days = week[0].range()
    assert len(days) == 7


def test_between_tuple(week):
    a, b = week[0].between_tuple()
    assert a < b
    assert b - a == timedelta(days=6, hours=23, minutes=59, seconds=59)


def test_middle(week):
    assert week[0].middle.dayname == 'torsdag'


def test_compare(week):
    assert ttcal.Week.weeknum() > week[0]
    assert ttcal.Week.weeknum(2015, 40) > ttcal.Week.weeknum(2015, 4)
    d14 = Day(2014, 10, 4)
    d15 = Day(2015, 10, 4)
    d16 = Day(2016, 10, 4)
    w = ttcal.Week.weeknum(2, 2015)
    y14 = ttcal.Year(2014)
    y15 = ttcal.Year(2015)
    y16 = ttcal.Year(2016)

    assert w > y14
    assert w < y16
    assert w == y15

    assert w < d16
    assert w <= d16
    assert w > d14
    assert w >= d14
    assert w == Day(2015, 1, 8)

    assert not w < None
    assert not w <= None
    assert not w == None
    assert not w >= None
    assert not w > None


def test_current(week):
    assert week[0].current is False
    assert ttcal.Today().week.current


def test_repr(week):
    assert repr(week[0]) == 'Week(4, month=1, year=2012)'


def test_until_today(week):
    w = ttcal.Today().week
    assert len(list(w.until_today())) == ttcal.Today() - w.first


def test_hash(week):
    assert hash(week[0]) == hash(week[-1])
    assert len(set(hash(w) for w in week)) == len(week) - 1  # first and last are equal
    assert hash(ttcal.Today() + 1) == hash(ttcal.Today().next())


def test_index(week):
    today = ttcal.Today()
    assert today in today.week
    assert today.week[0] <= today


def test_idtag(week):
    assert week[0].idtag() == 'w20124'
    assert week[1].idtag() == 'w%d1' % ttcal.Year()
    assert week[2].idtag() == 'w201252'


def test_datetuple(week):
    assert week[0].datetuple() == (2012, 1, 23)


def test_str(week):
    assert str(week[0]) == 'Uke 4 (2012)'
    assert str(week[2]) == 'Uke 52 (2012)'


def test_eq(week):
    """Test the __eq__ method defined in Week.
    """
    assert not (week[0] == week[1])
    assert week[0] == week[3]


def test_from_idtag(week):
    """Test the from_idtag method.
    """
    assert ttcal.Week.from_idtag('w20124') == week[0]


# @pytest.fixture
# def weeks():
#     return ttcal.Weeks(1, 10)  # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 (n=11)
#
#
# def test_weeks_first(weeks):
#     print weeks
#     assert weeks.first == ttcal.Year().first
#
#
# def test_weeks_last(weeks):
#     assert weeks.last == ttcal.Year().first + 70
#
#
# def test_datetuple(weeks):
#     assert weeks.datetuple() == ttcal.Year().first.datetuple()
