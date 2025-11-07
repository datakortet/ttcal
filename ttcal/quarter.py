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
        if isinstance(other, int):
            return self.quarter == other
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) == 0

    def __ne__(self, other: Any) -> bool:
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
        """Returns a datetime at 00:00:00 on January 1st.
        """
        d = datetime.date(*self.first.datetuple())
        t = datetime.time()
        return datetime.datetime.combine(d, t)

    @property
    def first(self) -> Day:
        # The negative indexing here is due to the fact that the
        # first quarter is list element 0 and so on.
        return self.Year.quarters()[self.quarter-1][0].first

    @property
    def last(self) -> Day:
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
        return f'Q({self.year}{self.quarter})'

    def __str__(self) -> str:  # pragma: nocover
        return str(self.quarter)

    @property
    def Quarter(self) -> Quarter:
        """Return the quarter (for api completeness).
        """
        return self

    @classmethod
    def from_idtag(cls, tag: str) -> Quarter:
        """quarter tags have the lower-case letter y + the four digit quarter,
           eg. q20081.
        """
        y = int(tag[1:5])
        q = int(tag[5])
        return cls(year=y, quarter=q)

    def idtag(self) -> str:
        """quarter tags have the lower-case letter y + the four digit quarter,
           eg. y2008.
        """
        return f'q{self.year}{self.quarter}'

    def __add__(self, n: int) -> Quarter:
        """Add n quarters to self.
        """
        return Quarter(self.year, self.quarter + n)

    def __radd__(self, n: int) -> Quarter:
        return self + n

    def __sub__(self, n: int) -> Quarter:
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
        return self.quarter

    def dayiter(self) -> Iterator[Day]:
        """Yield all days in all months in quarter.
        """
        for m in self.months:
            yield from m.days()

    def _format(self, fmtchars: List[str]) -> Iterator[str]:
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
           four-digit-year and quearter-number.
        """
        if fmt is None:
            fmt = "Q"
        tmp = list(self._format(list(fmt)))
        return ''.join(tmp)
