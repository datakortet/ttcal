from datetime import date, datetime
import ttcal
import pytest


@pytest.fixture
def halfyears():
    return [
        ttcal.Halfyear(2005, 1),
        ttcal.Halfyear(),
        ttcal.Halfyear(2025, 2),
    ]


def test_stringification(halfyears):
    assert str(halfyears[0]) == '1'


def test_timetuple(halfyears):
    assert halfyears[0].timetuple() == datetime(2005, 1, 1, 0, 0, 0)


def test_range(halfyears):
    assert len(list(halfyears[0].range())) == 90


def test_between_tuple(halfyears):
    a, b = halfyears[0].between_tuple()
    assert a < b


def test_middle(halfyears):
    assert halfyears[0].middle == (ttcal.Day(2005, 2, 14))


def test_unicode(halfyears):
    assert repr(halfyears[0]) == 'H(20051)'
    assert str(halfyears[0]) == '1'


def test_month(halfyears):
    assert halfyears[0].Month == ttcal.Month(2005, 1)


def test_halfyear(halfyears):
    assert int(halfyears[0]) == int(halfyears[0].Halfyear)


def test_hash(halfyears):
    assert hash(halfyears[0]) == hash(ttcal.Halfyear(2005, 1))


def test_from_idtag(halfyears):
    """Test of the from_idtag method.
    """
    assert halfyears[0].from_idtag('H20051') == halfyears[0]


def test_idtag(halfyears):
    """Test of the idtag method.
    """
    assert halfyears[2].idtag() == 'H20252'


def test_add(halfyears):
    """Test of the __add__ method.
    """
    assert halfyears[0] + 2 == ttcal.Halfyear(2005, 3)
    assert 2 + halfyears[0] == ttcal.Halfyear(2005, 3)


def test_sub(halfyears):
    """Test of the __sub__ method.
    """
    assert halfyears[2] - 3 == ttcal.Halfyear(2025, 1)


def test_prev(halfyears):
    """Test of the prev method.
    """
    assert halfyears[2].prev() == ttcal.Halfyear(2025, 3)


def test_next(halfyears):
    """Test of the next method.
    """
    assert halfyears[0].next() == ttcal.Halfyear(2005, 2)


def test_format(halfyears):
    assert halfyears[0].format('H') == '1'
    assert halfyears[0].format('H') == '2005H1'
    assert halfyears[0].format() == '2005H1'
