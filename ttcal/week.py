"""
Week class.
"""
from __future__ import annotations
from typing import Optional, List, Tuple, Iterator, Any, Union
import datetime
from .day import Day, Days
from .calfns import isoweek, rangecmp, rangetuple


class Week:
    """A single week in a Year.
    """
    year: Optional[int] = None
    num: Optional[int] = None
    days: Optional[List[Day]] = None
    month: Optional[int] = None

    def range(self) -> Days:
        """Return an iterator for the range of `self`.
        """
        return Days(self.first, self.last)

    def between_tuple(self) -> Tuple[datetime.datetime, datetime.datetime]:  # pylint:disable=E0213
        """Return a tuple of datetimes that is convenient for sql
           `between` queries.
        """
        return (self.first.datetime(),
                (self.last + 1).datetime() - datetime.timedelta(seconds=1))

    @property
    def middle(self) -> Day:
        """Return the day that splits the date range in half.
        """
        middle = (self.first.toordinal() + self.last.toordinal()) // 2
        return Day.fromordinal(middle)

    # def timetuple(self):
    #     """Create timetuple from datetuple.
    #        (to interact with datetime objects).
    #     """
    #     d = datetime.date(*self.datetuple())
    #     t = datetime.time()
    #     return datetime.datetime.combine(d, t)

    @classmethod
    def from_idtag(cls, tag: str) -> Week:
        """Parse tag and return a week object.
        """
        # w20081
        y = int(tag[1:5])
        w = int(tag[5:])
        return cls.weeknum(w, y)

    @classmethod
    def weeknum(cls, n: Optional[int] = None, year: Optional[int] = None) -> Week:
        """Return the ISO week number.
        """
        if n is None and year is None:
            year, n = datetime.date.today().isocalendar()[:2]
        if year is None:
            year = datetime.date.today().year
        days = list(isoweek(year, n))
        month = days[0].month  # quite arbitrary
        return cls(days, month)

    def __init__(self, days: List[Union[datetime.date, Day]], month: int) -> None:
        super().__init__()
        # thursday is always in the correct iso-year per definition
        t = days[3].isocalendar()
        self.year = t[0]
        self.num = t[1]
        self.days = [Day(d, membermonth=month) for d in days]
        self.month = month

    @property
    def current(self) -> bool:
        """True if today is in week.
        """
        return any(d.today for d in self.days)

    def idtag(self) -> str:
        """Return a tag representing this week.
        """
        return f'w{self.year}{self.num}'

    @property
    def first(self) -> Day:
        """1st day of week.
        """
        return self.days[0]

    @property
    def last(self) -> Day:
        """Last day of week.
        """
        return self.days[-1]

    def datetuple(self) -> Tuple[int, int, int]:
        """First day of this week.
        """
        return self.year, self.month, self.first.day

    def __str__(self) -> str:
        return f'Uke {self.num} ({self.year})'

    def __repr__(self) -> str:
        return f'Week({self.num}, month={self.month}, year={self.year})'

    def __iter__(self) -> Iterator[Day]:
        return iter(self.days)

    def until_today(self) -> Iterator[Day]:
        """Yield all days in week that are in the past.
        """
        for d in self.days:
            if d.today:
                break
            yield d

    def __hash__(self) -> int:
        return self.year * 100 + self.num

    def rangetuple(self) -> Tuple[datetime.datetime, datetime.datetime]:
        """Return a pair of datetime objects representing this week
           (as a half-open interval).
        """
        return self.days[0].rangetuple()[0], self.days[-1].rangetuple()[-1]

    def __lt__(self, other: Any) -> bool:
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) < 0

    def __le__(self, other: Any) -> bool:
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) <= 0

    def __eq__(self, other: Any) -> bool:
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) == 0

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __gt__(self, other: Any) -> bool:
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) > 0

    def __ge__(self, other: Any) -> bool:
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) >= 0

    # def __eq__(self, other):
    #     return self.year == other.year and self.num == other.num

    def __getitem__(self, n: int) -> Day:
        return self.days[n]

    def __contains__(self, date: Any) -> bool:
        return date in self.days


# class Weeks(list):
#     def __init__(self, start, end):
#         super(Weeks, self).__init__()
#         assert start <= end
#         for i in range(start, end + 1):
#             self.append(Week.weeknum(i))
#
#     def range(self):
#         """Return an iterator for the range of `self`.
#         """
#         return self.dayiter()
#
#     def between_tuple(self):  # pylint:disable=E0213
#         """Return a tuple of datetimes that is convenient for sql
#            `between` queries.
#         """
#         return (self.first.datetime(),
#                 (self.last + 1).datetime() - datetime.timedelta(seconds=1))
#
#     @property
#     def middle(self):
#         """Return the day that splits the date range in half.
#         """
#         middle = (self.first.toordinal() + self.last.toordinal()) // 2
#         return Day.fromordinal(middle)
#
#     def timetuple(self):
#         """Create timetuple from datetuple.
#            (to interact with datetime objects).
#         """
#         d = datetime.date(*self.datetuple())
#         t = datetime.time()
#         return datetime.datetime.combine(d, t)
#
#     @property
#     def first(self):
#         """First day in first week.
#         """
#         return self[0][0]
#
#     @property
#     def last(self):
#         """Last day in last week.
#         """
#         return self[-1][-1]
#
#     def datetuple(self):
#         """First day of first week.
#         """
#         return self.first.datetuple()
#
#     def dayiter(self):
#         """Iterate over all days in all the weeks.
#         """
#         for wk in self:
#             for day in wk:
#                 yield day
#
#     def __repr__(self):
#         return '[' + ', '.join(map(str, iter(self))) + ']'


def _Week(self: Day) -> Week:
    """Return a Week object representing the week `self` belongs to.
    """
    return Week.weeknum(self.weeknum, self.isoyear)


Day.week = property(_Week)
