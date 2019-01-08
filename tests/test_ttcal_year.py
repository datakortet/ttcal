# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from datetime import date, datetime
import ttcal
import pytest

try:
    unicode
except NameError:  # pragma: nocover
    unicode = str


@pytest.fixture
def years():
    return [
        ttcal.Year(2005),
        ttcal.Year(),
        ttcal.Year(2025),
    ]


def test_stringification(years):
    assert unicode(years[0]) == '2005'
    assert str(years[0]) == '2005'


def test_timetuple(years):
    assert years[0].timetuple() == datetime(2005, 1, 1, 0, 0, 0)


def test_range(years):
    assert len(list(years[0].range())) == 365


def test_between_tuple(years):
    a, b = years[0].between_tuple()
    assert a < b


def test_middle(years):
    assert years[0].middle == (ttcal.Day(2005, 1, 1) + 365 // 2)


def test_unicode(years):
    assert repr(years[0]) == 'Year(2005)'
    assert str(years[0]) == '2005'


def test_datetuple(years):
    assert years[0].datetuple()[:1] == years[0].Month.datetuple()[:1]


def test_month(years):
    assert years[0].Month == ttcal.Month(2005, 1)


def test_year(years):
    assert int(years[0]) == int(years[0].Year)


def test_rows(years):
    assert len(list(years[0].rows())) == 4
    assert len(list(years[0].rows4())) == 3


def test_hash(years):
    assert hash(years[0]) == hash(ttcal.Year(2005))


def test_from_idtag(years):
    """Test of the from_idtag method.
    """
    assert years[0].from_idtag('y2005') == years[0]


def test_idtag(years):
    """Test of the idtag method.
    """
    assert years[2].idtag() == 'y2025'


def test_add(years):
    """Test of the __add__ method.
    """
    assert years[0] + 5 == ttcal.Year(2010)
    assert 5 + years[0] == ttcal.Year(2010)


def test_sub(years):
    """Test of the __sub__ method.
    """
    assert years[0] - 3 == ttcal.Year(2002)


def test_prev(years):
    """Test of the prev method.
    """
    assert years[0].prev() == ttcal.Year(2004)


def test_next(years):
    """Test of the next method.
    """
    assert years[0].next() == ttcal.Year(2006)


def test_periods(years):
    """Test of periods using misc methods and properties.
    """
    first_half = [ttcal.Month(2005, 1), ttcal.Month(2005, 2),
                  ttcal.Month(2005, 3), ttcal.Month(2005, 4),
                  ttcal.Month(2005, 5), ttcal.Month(2005, 6)]
    Q3 = [ttcal.Month(2005, 7), ttcal.Month(2005, 8), ttcal.Month(2005, 9)]
    assert years[0].H1 == first_half
    assert years[0].Q3 == Q3

    assert years[0].halves()
    assert years[0].quarters()
    assert years[0].january
    assert years[0].february
    assert years[0].march
    assert years[0].april
    assert years[0].may
    assert years[0].june
    assert years[0].july
    assert years[0].august
    assert years[0].september
    assert years[0].october
    assert years[0].november
    assert years[0].december


def test_mark_period(years):
    """Test the mark_period method.
    """
    res = [ttcal.Day(2025, 3, 1), ttcal.Day(2025, 3, 2),
           ttcal.Day(2025, 3, 3)]
    years[2].mark_period(years[2].march)
    days = []
    for i, day in enumerate(years[2].marked_days()):
        days.append(day)
        if i == 2:
            break
    assert days == res


def test_cmp(years):
    """Test the compare methods.
    """
    assert years[1] == ttcal.Year(date.today().year)
    assert not (years[0] == years[2])
    # assert not (years[0] == 'foo')
    assert ttcal.Year(2015) < ttcal.Year(2016)
    assert ttcal.Year(2015) <= ttcal.Year(2016)
    assert ttcal.Year(2016) > ttcal.Year(2015)
    assert ttcal.Year(2016) >= ttcal.Year(2015)
    assert ttcal.Year(2015) == ttcal.Week.weeknum(1, 2015)
    assert not ttcal.Year(2015) in [None]
    assert not ttcal.Year(2015) < None
    assert not ttcal.Year(2015) <= None
    assert not ttcal.Year(2015) is None
    assert not ttcal.Year(2015) > None
    assert not ttcal.Year(2015) >= None


def test_contains(years):
    assert years[0].middle in years[0]


def test_mark(years):
    y = ttcal.Year()
    m = y.middle
    y.mark(m, 'foo')
    # assert 'foo' in m.display
    assert True  # ??


def test_format(years):
    assert years[0].format('Yyx') == '200505x'
    assert years[0].format() == '2005'
