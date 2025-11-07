"""
Year class.
"""
from __future__ import annotations
from typing import Optional, List, Tuple, Union, Iterator, Any
import datetime
from .calfns import chop, rangecmp, rangetuple
from .day import Day
from .month import Month


class Year:  # pylint:disable=too-many-public-methods
    """A single year.
    """
    year: int
    months: List[Month]

    def __init__(self, year: Optional[int] = None) -> None:
        super().__init__()
        if year is None:
            year = datetime.date.today().year
        self.year = year
        self.months = [Month(year, i + 1) for i in range(12)]

    def __int__(self) -> int:
        return self.year

    def range(self) -> Iterator[Day]:
        """Return an iterator for the range of `self`.
        """
        return self.dayiter()

    def rangetuple(self) -> Tuple[datetime.datetime, datetime.datetime]:
        """Return a pair of datetime objects containing year
           (in a half-open interval).
        """
        return self.first.datetime(), (self + 1).first.datetime()

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.year < other
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) < 0

    def __le__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.year <= other
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) <= 0

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.year == other
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) == 0

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.year > other
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) > 0

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.year >= other
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) >= 0

    def timetuple(self) -> datetime.datetime:
        """Returns a datetime at 00:00:00 on January 1st.
        """
        d = datetime.date(*self.first.datetuple())
        t = datetime.time()
        return datetime.datetime.combine(d, t)

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

    def __repr__(self) -> str:
        return f'Year({self.year})'

    def __str__(self) -> str:  # pragma: nocover
        return str(self.year)

    @property
    def Month(self) -> Month:
        """For orthogonality in the api.
        """
        return self.months[0]

    @property
    def Year(self) -> Year:
        """Return the year (for api completeness).
        """
        return self

    @classmethod
    def from_idtag(cls, tag: str) -> Year:
        """Year tags have the lower-case letter y + the four digit year,
           eg. y2008.
        """
        y = int(tag[1:5])
        return cls(year=y)

    def idtag(self) -> str:
        """Year tags have the lower-case letter y + the four digit year,
           eg. y2008.
        """
        return f'y{self.year}'

    def marked_days(self) -> Iterator[Day]:
        """Yield all 'marked' days in year.
        """
        for m in self.months:
            yield from m.marked_days()

    def datetuple(self) -> Tuple[int, None, None]:
        """January 1.
        """
        return self.year, None, None

    def __add__(self, n: int) -> Year:
        """Add n years to self.
        """
        return Year(self.year + n)

    def __radd__(self, n: int) -> Year:
        return self + n

    def __sub__(self, n: int) -> Year:
        return self + (-n)

    # rsub doesn't make sense

    def prev(self) -> Year:
        """Previous year.
        """
        return self - 1

    def next(self) -> Year:
        """Next year.
        """
        return self + 1

    @property
    def H1(self) -> List[Month]:
        """First half of this year.
        """
        return self.months[:6]

    @property
    def H2(self) -> List[Month]:
        """Last half of this year.
        """
        return self.months[6:]

    def halves(self) -> List[List[Month]]:
        """Both halves of the year.
        """
        return [self.H1, self.H2]

    @property
    def Q1(self) -> List[Month]:
        """1st quarter.
        """
        return self.months[:3]

    @property
    def Q2(self) -> List[Month]:
        """2nd quarter.
        """
        return self.months[3:6]

    @property
    def Q3(self) -> List[Month]:
        """3rd quarter.
        """
        return self.months[6:9]

    @property
    def Q4(self) -> List[Month]:
        """4th quarter.
        """
        return self.months[9:]

    def quarters(self) -> List[List[Month]]:
        """Every quarter in this year.
        """
        return [self.Q1, self.Q2, self.Q3, self.Q4]

    # pylint:disable=C0111
    @property
    def january(self) -> Month:
        return self.months[0]

    @property
    def february(self) -> Month:
        return self.months[1]

    @property
    def march(self) -> Month:
        return self.months[2]

    @property
    def april(self) -> Month:
        return self.months[3]

    @property
    def may(self) -> Month:
        return self.months[4]

    @property
    def june(self) -> Month:
        return self.months[5]

    @property
    def july(self) -> Month:
        return self.months[6]

    @property
    def august(self) -> Month:
        return self.months[7]

    @property
    def september(self) -> Month:
        return self.months[8]

    @property
    def october(self) -> Month:
        return self.months[9]

    @property
    def november(self) -> Month:
        return self.months[10]

    @property
    def december(self) -> Month:
        return self.months[11]

    def dayiter(self) -> Iterator[Day]:
        """Yield all days in all months in year.
        """
        for m in self.months:
            yield from m.days()

    def days(self) -> List[Day]:
        """Yield all days in all months in year.
        """
        return list(self.dayiter())

    @property
    def daycount(self) -> int:
        """Return the number of days in year.
        """
        return len(self.days())

    def rows(self) -> Iterator[List[Month]]:
        """Return a year calendar layout (3x4).
        """
        return chop(iter(self.months), 3)

    def rows4(self) -> Iterator[List[Month]]:
        """Return a year calendar layout (4x3).
        """
        return chop(iter(self.months), 4)

    @property
    def first(self) -> Day:
        """First day of first month.
        """
        return self.months[0].first

    @property
    def last(self) -> Day:
        """Last day of last month.
        """
        return self.months[-1].last

    def __hash__(self) -> int:
        return self.year

    # def __eq__(self, other):
    #     if hasattr(other, 'year'):
    #         return self.year == other.year
    #     return False

    def __contains__(self, date: Any) -> bool:
        return date.year == self.year

    def __getitem__(self, day: Day) -> Day:
        m = self.months[day.month - 1]
        return m[day]

    def mark_period(self, p: Any, value: str = 'mark') -> None:
        """Add a 'mark' to a series (period) of days in year.
        """
        d = p.first
        while d != p.last:
            self.mark(d, value)
            d += 1
        self.mark(p.last, value)

    def mark(self, d: Day, value: str = 'mark') -> None:
        """Add a 'mark' to a day in this year.
        """
        try:
            self[d].mark = value
        except KeyError:  # pragma:nocover
            pass

    def _format(self, fmtchars: List[str]) -> Iterator[str]:
        # http://blog.tkbe.org/archive/date-filter-cheat-sheet/
        for ch in fmtchars:
            if ch == 'y':
                yield str(self.year)[-2:]
            elif ch == 'Y':
                yield str(self.year)
            else:
                yield ch

    def format(self, fmt: Optional[str] = None) -> str:
        """Format according to format string. Default format is
           monthname, four-digit-year.
        """
        if fmt is None:
            fmt = "Y"
        tmp = list(self._format(list(fmt)))
        return ''.join(tmp)


# noinspection PyPep8Naming
def _Day_Year(self: Day) -> Year:
    """Return a Year object representing the year `self` belongs to.
    """
    return Year(self.year)


Day.Year = property(_Day_Year)


# noinspection PyPep8Naming
def _Month_Year(self: Month) -> Year:
    """Return a Year object for the year-part of this month.
    """
    return Year(self.year)


Month.Year = property(_Month_Year)
