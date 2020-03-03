# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from datetime import date, datetime
import pickle
import ttcal
import pytest

try:
    unicode
except NameError:  # pragma: nocover
    unicode = str



@pytest.fixture
def months():
    return [
        ttcal.Month(2012, 4),
        ttcal.Month(year=2012, month=10),
        ttcal.Month(date=date(2012, 7, 10)),
    ]


def test_stringification(months):
    assert unicode(months[0]) == '2012-04'
    assert str(months[0]) == '2012-04'


def test_range(months):
    assert len(list(months[0].range())) == 30


def test_between_tuple(months):
    a, b = months[0].between_tuple()
    assert a < b


def test_rangetuple(months):
    a, b = months[0].rangetuple()
    assert a < b


def test_compare(months):
    a, b = ttcal.Month(2015, 10), ttcal.Month(2013, 3)
    print("ab:", a > b)
    print("ab:", a > b)
    print("Month compare:", ttcal.Month(2015, 10) > ttcal.Month(2013, 3))
    print("Month compare:", ttcal.Month(2015, 10) > ttcal.Month(2013, 3))
    assert ttcal.Month(2015, 10) > ttcal.Month(2013, 3)
    assert ttcal.Month() > months[0]
    assert months[0] < months[1]
    assert months[0] <= months[1]
    assert months[1] > months[0]
    assert months[1] >= months[0]
    assert ttcal.Day(2015, 1, 1) < ttcal.Month(2015, 2)
    assert ttcal.Day(2015, 1, 1) <= ttcal.Month(2015, 2)
    assert ttcal.Day(2015, 2, 1) == ttcal.Month(2015, 2)
    assert ttcal.Day(2015, 3, 1) >= ttcal.Month(2015, 2)
    assert ttcal.Day(2015, 3, 1) > ttcal.Month(2015, 2)

    assert not ttcal.Month(2015, 1) < None
    assert not ttcal.Month(2015, 1) <= None
    assert not ttcal.Month(2015, 1) == None
    assert not ttcal.Month(2015, 1) > None
    assert not ttcal.Month(2015, 1) >= None


def test_middle(months):
    assert months[0].middle == months[0].first + 14


def test_next(months):
    assert months[0].next() == months[0] + 1


def test_parse(months):
    """ttcal.Month.parse(txt)
    """
    assert ttcal.Month.parse('2012-04') == months[0]
    assert ttcal.Month.parse('2012-4') == months[0]
    assert ttcal.Month.parse('2012-09') == ttcal.Month(2012, 9)
    assert ttcal.Month.parse("") is None

    with pytest.raises(ValueError):
        ttcal.Month.parse('12-04')


def test_ctor(months):
    assert ttcal.Month() == ttcal.Today().Month

    with pytest.raises(ValueError):
        ttcal.Month(2012, 15)


def test_pickle(months):
    assert months == pickle.loads(pickle.dumps(months))


def test_call(months):
    assert months[0].first == ttcal.Year(2012).april(1)


def test_from_idtag(months):
    """Test the from_idtag method.
    """
    assert ttcal.Month.from_idtag('m201204') == months[0]


def test_from_date(months):
    """Test the from_date method.
    """
    assert ttcal.Month.from_date(date(2012, 7, 10)) == months[2]
    assert ttcal.Month.from_date(date(2012, 10, 20)) == months[1]


def test_Year(months):
    """Test the Year method.
    """
    assert months[0].Year == ttcal.Year(2012)
    assert months[0].Month == months[0]


def test_hash(months):
    assert hash(ttcal.Today().Month) == hash(ttcal.Month())


def test_unicode(months):
    assert repr(months[0]) == 'Month(2012, 4)'
    assert str(months[0]) == '2012-04'


def test_qmp(months):
    """Test the cmp methods.
    """
    assert months[0] == date(2012, 4, 5)
    assert not (months[1] == months[0])
    # assert not (months[0] == 'foo')


def test_len(months):
    """Test the __len__ method.
    """
    assert len(months[0]) == 30


def test_numdays(months):
    """Test the numdays method.
    """
    assert months[1].numdays() == 31


def test_add(months):
    """Test the __add__ method.
    """
    assert months[0] + 3 == ttcal.Month(2012, 7)
    assert 3 + months[0] == ttcal.Month(2012, 7)


def test_sub(months):
    """Test the __sub__ method.
    """
    assert months[0] - 3 == ttcal.Month(2012, 1)
    assert months[0] - months[0] == 0
    assert months[0] - months[0].prev() == 1
    assert months[0].prev() - months[0] == -1


def test_daycount2():
    assert ttcal.Month(2012, 2).daycount == 29


def test_dayiter(months):
    """Test the dayiter method.
    """
    res = [ttcal.Day(2012, 6, 25), ttcal.Day(2012, 6, 26),
           ttcal.Day(2012, 6, 27)]
    days = []
    for i, day in enumerate(months[2].dayiter()):
        days.append(day)
    assert days[:3] == res


def test_days(months):
    """Test the days method.
    """
    res = [ttcal.Day(2012, 7, 1), ttcal.Day(2012, 7, 2),
           ttcal.Day(2012, 7, 3)]
    assert months[2].days()[:3] == res


def test_idtag(months):
    """Test the idtag method.
    """
    assert months[2].idtag() == 'm20127'


def test_daycount(months):
    """Test the daycount property.
    """
    assert months[2].daycount == 31


def test_marked_days(months):
    """Test the mark method.
    """
    res = [ttcal.Day(2012, 10, 3), ttcal.Day(2012, 10, 10)]
    months[1].mark(ttcal.Day(2012, 10, 10))
    months[1].mark(ttcal.Day(2012, 10, 10), value='appended', method='append')
    months[1].mark(ttcal.Day(2012, 10, 3))
    days = []
    for day in months[1].marked_days():
        days.append(day)
    assert days == res


def test_format(months):
    """Test the format method.
    """
    assert months[0].format() == 'April, 2012'
    assert months[0].format('F-Y') == 'April-2012'
    assert months[0].format('n y') == '4 12'
    assert months[0].format('m') == '04'
    assert months[0].format('b') == 'apr'
    assert months[0].format('M') == 'Apr'


def test_timetuple():
    assert ttcal.Month(2015, 10).timetuple() == datetime(2015, 10, 1, 0)


def test_contains():
    assert ttcal.Today() in ttcal.Month()

    with pytest.raises(KeyError):
        (ttcal.Month() + 2)[ttcal.Today()]


def test_mark(months):
    m = ttcal.Month()
    d = m.first
    m.mark(d, 'foo')
    assert m[d].mark == 'foo'
    m.mark(d, 'bar', 'append')
    assert m[d].mark == 'foobar'
    e = m.last
    m.mark(e, 'baz', 'append')
    assert m[e].mark == 'baz'

    # with pytest.raises(KeyError):
    #     m.mark(ttcal.Day(2000, 1, 1), 'foobarbaz')
