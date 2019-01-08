# -*- coding: utf-8 -*-
from datetime import date, datetime
from unittest import TestCase
import pickle
import six
import ttcal
import pytest


@pytest.fixture
def days():
    return [
        ttcal.Day(date(2012, 4, 10)),
        ttcal.Day(2012, 4, 8),
        ttcal.Day(),
        ttcal.Today(),
    ]


def test_reduce(days):
    assert pickle.loads(pickle.dumps(days)) == days


def test_from_idtag(days):
    assert ttcal.Day.from_idtag("d20120410") == days[0]


def test_parse():
    assert ttcal.Day.parse("") is None
    assert ttcal.Day.parse('02051970') == ttcal.Day(1970, 5, 2)


def test_ctor_raises():
    with pytest.raises(TypeError):
        ttcal.Day(1,2,3,4,5)


def test_range(days):
    assert len(days[1].range()) == 1


def test_between_tuple(days):
    t = days[1].between_tuple()
    assert t[0] <= days[1].datetime()
    assert days[1].datetime() <= t[1]


def test_middle(days):
    assert days[1].middle == days[1]


def test_cmp():
    assert not ttcal.Day(2015, 1, 1) < None
    assert not ttcal.Day(2015, 1, 1) <= None
    assert not ttcal.Day(2015, 1, 1) == None
    assert not ttcal.Day(2015, 1, 1) > None
    assert not ttcal.Day(2015, 1, 1) >= None


def test_repr(days):
    assert repr(days[1]) == '2012-4-8-4'
    assert str(days[1]) == '2012-04-08'


def test_date(days):
    assert type(days[1].date()) == date


def test_next_prev(days):
    assert days[1].next() == days[1] + 1
    assert days[1].prev() == days[1] - 1


def test_sub(days):
    assert days[0] - days[1] == 2
    assert days[0] - ttcal.Duration(days=2) == days[1]

    with pytest.raises(ValueError):
        days[0] - 'foo'


def test_timetuple(days):
    assert isinstance(days[0].timetuple(), datetime)
    assert ttcal.Today().timetuple() == ttcal.Day().timetuple()


def test_display(days):
    d = ttcal.Today()
    d.mark = 'foo'
    assert 'foo' in d.display
    noday = ttcal.Day.from_idtag('d201502011')
    assert 'noday' in noday.display
    assert noday.special is False


def test_days_startweek(days):
    dd = ttcal.Days(days[1], days[0], start_week=True)
    assert dd.first <= days[1]
    assert dd.last == days[0]


def test_days_between_tuple(days):
    dd = ttcal.Days(days[1], days[0])
    a, b = dd.between_tuple()
    assert a < b


class TestDay(TestCase):
    """Unit tests for the ttcal.Day class.
    """

    def setUp(self):
        """SetUp default data for the tests.
        """
        self.day1 = ttcal.Day(date(2012, 4, 10))
        self.day2 = ttcal.Day(2012, 4, 8)
        self.day3 = ttcal.Day()
        self.today = ttcal.Today()

    def test_get_day_name(self):
        """Test of the get_day_name method.
        """
        assert self.day1.get_day_name(2) == 'onsdag'
        assert self.day2.get_day_name(2, 3) == 'ons'

    def test_hash_(self):
        """Test of the __hash__ method.
        """
        # hash(x) truncates the returned value from __hash__ in Python 3..
        assert hash(self.day1) == hash(hash(self.day1))
        assert hash(self.day1) == hash(self.day1)

    def test_unicode_(self):
        """Test of the __unicode__ method.
        """
        assert six.text_type(self.day2) == six.u('2012-04-08')

    def test_datetuple(self):
        """Test of the datetuple method.
        """
        assert self.day2.datetuple() == tuple((2012, 4, 8))

    def test_add_(self):
        """Test of the __add__ method.
        """
        assert self.day2 + 3 == ttcal.Day(2012, 4, 11)

    def test_sub_(self):
        """Test of the __sub__ method.
        """
        assert self.day1 - 5 == ttcal.Day(2012, 4, 5)

    def test_day_name(self):
        """Test of the day_name property.
        """
        assert self.day1.dayname == 'tirsdag'
        assert self.day2.dayname == u'søndag'

    def test_code(self):
        """Test of the code property.
        """
        assert self.day1.code == 'U'

    def test_weeknum(self):
        """Test of the weeknum property.
        """
        assert self.day1.weeknum == 15

    def test_isoyear(self):
        """Test of the isoyear property.
        """
        assert self.day1.isoyear == 2012

    def test_week(self):
        """Test of the week property.
        """
        week = ttcal.Week.weeknum(15, 2012)
        assert self.day1.week == week

    def test_Month(self):
        """Test of the Month property.
        """
        month = ttcal.Month(2012, 4)
        assert self.day1.Month == month

    def test_Year(self):
        """Test of the Year property.
        """
        year = ttcal.Year(2012)
        assert self.day1.Year == year

    def test_display(self):
        """Test of the display property.
        """
        #assert self.day3.display, 'today month')
        assert ('today' in self.day3.display)
        assert ('month' in self.day3.display)

    def test_idtag(self):
        """Test of the idtag property.
        """
        assert self.day1.idtag == 'd2012041004'

    def test_today(self):
        """Test of the today property.
        """
        assert self.day3.today
        assert self.day1.today == False

    def test_weekday(self):
        """Test of the weekday property.
        """
        assert self.day1.weekday
        assert self.day2.weekday != True # Does not return False

    def test_weekend(self):
        """Test of the weekend property.
        """
        assert self.day2.weekend
        assert not self.day1.weekend

    def test_in_month(self):
        """Test of the in_month property.
        """
        assert (self.day3.in_month)

    def test_compare(self):
        """Test the compare method.
        """
        assert self.day1.compare(self.day2) == 'month'
        assert self.day1.compare(None) is None

    def test_compare_specific(self):
        """Test the methods in the CompareMixin class.
        """
        assert (self.day1 > self.day2)
        assert not (self.day1 < self.day2)
        assert not (self.day1 <= self.day2)
        assert (self.day1 >= self.day2)
        assert not (self.day1 == self.day2)
        assert (self.day1 != self.day2)

    def test_format(self):
        """Test the format method.
        """
        assert self.day1.format('y-m-d') == '12-04-10'
        assert self.day1.format('Y-W') == '2012-15'
        assert self.day1.format('b') == 'apr'
        assert self.day1.format('w') == '1'
        assert self.day1.format('D-n') == 'tir-4'
        assert self.day1.format('z') == '100'
        assert self.day1.format() == u'Apr 10, 2012'

    def test_from_idtag(self):
        """Test the from_idtag method.
        """
        assert ttcal.Day.from_idtag('d2012041004') == self.day1

    def test_parse(self):
        """Test the parse method.
        """
        assert self.day1.parse('04/08/2011') == ttcal.Day(2011, 8, 4)
        assert self.day1.parse('2012-04-06') == ttcal.Day(2012, 4, 6)
        assert self.day1.parse('2012-4-6') == ttcal.Day(2012, 4, 6)
        assert self.day1.parse('20130619') == ttcal.Day(2013, 6, 19)
        assert self.day1.parse('12.11.2013') == ttcal.Day(2013, 11, 12)
        assert self.day1.parse('12.10.13') == ttcal.Day(2013, 10, 12)

        self.assertRaises(ValueError, self.day1.parse, '12.10.11')
        self.assertRaises(ValueError, self.day1.parse, '21/13/2011')


class TestDays(TestCase):
    """Unit tests for the ttcal.Days class.
    """

    def setUp(self):
        """SetUp default data for the tests.
        """
        self.days = ttcal.Days(date(2012, 1, 1), date(2012, 1, 10))

    def test_first(self):
        """Test the first property.
        """
        first = self.days.first
        assert [first.year, first.month, first.day] == [2012, 1, 1]

    def test_middle(self):
        """Test the middle property.
        """
        middle = self.days.middle
        assert [middle.year, middle.month, middle.day] == [2012, 1, 5]

    def test_last(self):
        """Test the last property.
        """
        last = self.days.last
        assert [last.year, last.month, last.day] == [2012, 1, 10]

    def test_range(self):
        """The the range method defined in the RangeMixin class.
        """
        res = [ttcal.Day(2012, 1, 1), ttcal.Day(2012, 1, 2),
               ttcal.Day(2012, 1, 3), ttcal.Day(2012, 1, 4),
               ttcal.Day(2012, 1, 5), ttcal.Day(2012, 1, 6),
               ttcal.Day(2012, 1, 7), ttcal.Day(2012, 1, 8),
               ttcal.Day(2012, 1, 9), ttcal.Day(2012, 1, 10)]
        assert self.days.range() == res
