from datetime import date, datetime
import ttcal
import pytest


@pytest.fixture
def quarters():
    return [
        ttcal.Quarter(2005, 1),
        ttcal.Quarter(),
        ttcal.Quarter(2025, 4),
    ]


def test_stringification(quarters):
    assert str(quarters[0]) == '1'


def test_timetuple(quarters):
    assert quarters[0].timetuple() == datetime(2005, 1, 1, 0, 0, 0)


def test_range(quarters):
    assert len(list(quarters[0].range())) == 90


def test_between_tuple(quarters):
    a, b = quarters[0].between_tuple()
    assert a < b


def test_middle(quarters):
    assert quarters[0].middle == (ttcal.Day(2005, 2, 14))


def test_unicode(quarters):
    assert repr(quarters[0]) == 'Q(20051)'
    assert str(quarters[0]) == '1'


def test_month(quarters):
    assert quarters[0].Month == ttcal.Month(2005, 1)


def test_quarter(quarters):
    assert int(quarters[0]) == int(quarters[0].Quarter)


def test_hash(quarters):
    assert hash(quarters[0]) == hash(ttcal.Quarter(2005, 1))


def test_from_idtag(quarters):
    """Test of the from_idtag method.
    """
    assert quarters[0].from_idtag('q20051') == quarters[0]


def test_idtag(quarters):
    """Test of the idtag method.
    """
    assert quarters[2].idtag() == 'q20254'


def test_add(quarters):
    """Test of the __add__ method.
    """
    assert quarters[0] + 2 == ttcal.Quarter(2005, 3)
    assert 2 + quarters[0] == ttcal.Quarter(2005, 3)


def test_sub(quarters):
    """Test of the __sub__ method.
    """
    assert quarters[2] - 3 == ttcal.Quarter(2025, 1)


def test_prev(quarters):
    """Test of the prev method.
    """
    assert quarters[2].prev() == ttcal.Quarter(2025, 3)


def test_next(quarters):
    """Test of the next method.
    """
    assert quarters[0].next() == ttcal.Quarter(2005, 2)


def test_format(quarters):
    assert quarters[0].format('q') == '1'
    assert quarters[0].format('Q') == '2005Q1'
    assert quarters[0].format() == '2005Q1'
