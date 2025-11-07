"""
quarter class.
"""
from __future__ import annotations
from typing import Optional, List, Tuple, Iterator, Any
import datetime

from .calfns import rangecmp, rangetuple
from .day import Day
from .year import Year


class Quarter:  # pylint:disable=too-many-public-methods
    """A single quarter.
    """
    year: int
    quarter: int
    months: List[Any]  # List[Month]

    def __init__(self, year: Optional[int] = None, quarter: Optional[int] = None) -> None:
        """Initialize a Quarter object.

           Args:
               year: The year number. If None, uses the current year.
               quarter: The quarter number (1-4). If None, uses quarter 1.
        """
        super().__init__()
        # if quarter is None:
        if year is None:
            year = datetime.date.today().year
        if quarter is None:
            quarter = 1
        self.year = year
        self.quarter = quarter
        self.months = Year(year).quarters()[self.quarter-1]

    def __int__(self) -> int:
        """Convert Quarter to integer representation.
        """
        return self.quarter

    def range(self) -> Iterator[Day]:
        """Return an iterator for the range of `self`.
        """
        return self.dayiter()

    def rangetuple(self) -> Tuple[datetime.datetime, datetime.datetime]:
        """Return a pair of datetime objects containing quarter
           (in a half-open interval).
        """
        return self.first.datetime(), (self + 1).first.datetime()

    # def __lt__(self, other):
    #     if isinstance(other, int):
    #         return self.quarter < other
    #     othr = rangetuple(other)
    #     if othr is other:
    #         return False
    #     return rangecmp(self.rangetuple(), othr) < 0
    #
    # def __le__(self, other):
    #     if isinstance(other, int):
    #         return self.quarter <= other
    #     othr = rangetuple(other)
    #     if othr is other:
    #         return False
    #     return rangecmp(self.rangetuple(), othr) <= 0

    def __eq__(self, other: Any) -> bool:
        """Compare if this quarter is equal to another quarter or time range.
        """
        if isinstance(other, int):
            return self.quarter == other
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) == 0

    def __ne__(self, other: Any) -> bool:
        """Compare if this quarter is not equal to another quarter or time range.
        """
        return not self == other

    # def __gt__(self, other):
    #     if isinstance(other, int):
    #         return self.quarter > other
    #     othr = rangetuple(other)
    #     if othr is other:
    #         return False
    #     return rangecmp(self.rangetuple(), othr) > 0
    #
    # def __ge__(self, other):
    #     if isinstance(other, int):
    #         return self.quarter >= other
    #     othr = rangetuple(other)
    #     if othr is other:
    #         return False
    #     return rangecmp(self.rangetuple(), othr) >= 0

    def timetuple(self) -> datetime.datetime:
        """Return a datetime at 00:00:00 on the first day of the quarter.
        """
        d = datetime.date(*self.first.datetuple())
        t = datetime.time()
        return datetime.datetime.combine(d, t)

    @property
    def first(self) -> Day:
        """Return the first day of the quarter.
        """
        # The negative indexing here is due to the fact that the
        # first quarter is list element 0 and so on.
        return self.Year.quarters()[self.quarter-1][0].first

    @property
    def last(self) -> Day:
        """Return the last day of the quarter.
        """
        return self.Year.quarters()[self.quarter-1][2].last

    def between_tuple(self) -> Tuple[datetime.datetime, datetime.datetime]:  # pylint:disable=E0213
        """Return a tuple of datetimes that is convenient for sql
           `between` queries.
        """
        return (self.first.datetime(),
                (self.last + 1).datetime() - datetime.timedelta(seconds=1))

    @property
    def Year(self) -> Year:
        """Return the year (for api completeness).
        """
        return Year(self.year)

    @property
    def Month(self) -> Any:  # Month
        """For orthogonality in the api.
        """
        return self.months[0]

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
        """Return string representation for debugging.
        """
        return f'Q({self.year}{self.quarter})'

    def __str__(self) -> str:  # pragma: nocover
        """Return string representation of the quarter.
        """
        return str(self.quarter)

    @property
    def Quarter(self) -> Quarter:
        """Return the quarter (for api completeness).
        """
        return self

    @classmethod
    def from_idtag(cls, tag: str) -> Quarter:
        """Parse quarter tag and return a Quarter object.

           Format: 'q' followed by 4-digit year and quarter number.
           Example: q20081 represents Q1 of 2008.
        """
        y = int(tag[1:5])
        q = int(tag[5])
        return cls(year=y, quarter=q)

    def idtag(self) -> str:
        """Return a tag representing this quarter.

           Format: 'q' + year + quarter number (e.g., 'q20081').
        """
        return f'q{self.year}{self.quarter}'

    def __add__(self, n: int) -> Quarter:
        """Add n quarters to self.
        """
        return Quarter(self.year, self.quarter + n)

    def __radd__(self, n: int) -> Quarter:
        """Add n quarters to self (reverse operation).
        """
        return self + n

    def __sub__(self, n: int) -> Quarter:
        """Subtract n quarters from self.
        """
        return self + (-n)

    # rsub doesn't make sense

    def prev(self) -> Quarter:
        """Previous quarter.
        """
        return self - 1

    def next(self) -> Quarter:
        """Next quarter.
        """
        return self + 1

    def __hash__(self) -> int:
        """Return hash value for this quarter.
        """
        return self.quarter

    def dayiter(self) -> Iterator[Day]:
        """Yield all days in all months in quarter.
        """
        for m in self.months:
            yield from m.days()

    def _format(self, fmtchars: List[str]) -> Iterator[str]:
        """Internal formatting helper method.
        """
        # http://blog.tkbe.org/archive/date-filter-cheat-sheet/
        for ch in fmtchars:
            if ch == 'q':
                yield str(self.quarter)
            elif ch == 'Q':
                yield f'{str(self.year)}Q{self.quarter}'
            else:
                yield ch

    def format(self, fmt: Optional[str] = None) -> str:
        """Format according to format string. Default format is
           four-digit-year and quarter-number.
        """
        if fmt is None:
            fmt = "Q"
        tmp = list(self._format(list(fmt)))
        return ''.join(tmp)
