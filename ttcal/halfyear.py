"""
halfyear class.
"""
import datetime

from . import Month
from .calfns import chop, rangecmp, rangetuple
from .day import Day
from .year import Year


class Halfyear:  # pylint:disable=too-many-public-methods
    """A single halfyear.
    """
    def __init__(self, year=None, halfyear=None):
        super().__init__()
        # if quarter is None:
        if year is None:
            year = datetime.date.today().year
        if halfyear is None:
            halfyear = 1
        self.year = year
        self.halfyear = halfyear
        self.months = Year(year).halfyears()[self.halfyear-1]

    def __int__(self):
        return self.halfyear

    def range(self):
        """Return an iterator for the range of `self`.
        """
        return self.dayiter()

    def rangetuple(self):
        """Return a pair of datetime objects containing halfyear
           (in a half-open interval).
        """
        return self.first.datetime(), (self + 1).first.datetime()

    # def __lt__(self, other):
    #     if isinstance(other, int):
    #         return self.halfyear < other
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

    def __eq__(self, other):
        if isinstance(other, int):
            return self.halfyear == other
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) == 0

    def __ne__(self, other):
        return not self == other

    # def __gt__(self, other):
    #     if isinstance(other, int):
    #         return self.halfyear > other
    #     othr = rangetuple(other)
    #     if othr is other:
    #         return False
    #     return rangecmp(self.rangetuple(), othr) > 0
    #
    # def __ge__(self, other):
    #     if isinstance(other, int):
    #         return self.halfyear >= other
    #     othr = rangetuple(other)
    #     if othr is other:
    #         return False
    #     return rangecmp(self.rangetuple(), othr) >= 0

    def timetuple(self):
        """Returns a datetime at 00:00:00 on January 1st.
        """
        d = datetime.date(*self.first.datetuple())
        t = datetime.time()
        return datetime.datetime.combine(d, t)

    @property
    def first(self):
        # The negative indexing here is due to the fact that the
        # first halfyear is list element 0 and so on.
        return self.Year.halfyears()[self.halfyear-1][0].first

    @property
    def last(self):
        return self.Year.halfyears()[self.halfyear-1][2].last

    def between_tuple(self):  # pylint:disable=E0213
        """Return a tuple of datetimes that is convenient for sql
           `between` queries.
        """
        return (self.first.datetime(),
                (self.last + 1).datetime() - datetime.timedelta(seconds=1))

    @property
    def Year(self):
        """Return the year (for api completeness).
        """
        return Year(self.year)

    @property
    def Month(self):
        """For orthogonality in the api.
        """
        return self.months[0]

    @property
    def middle(self):
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

    def __repr__(self):
        return f'H({self.year}{self.halfyear})'

    def __str__(self):  # pragma: nocover
        return str(self.halfyear)

    @property
    def Halfyear(self):
        """Return the halfyear (for api completeness).
        """
        return self

    @classmethod
    def from_idtag(cls, tag):
        """halfyear tags have the upper-case letter H + the four digit year,
           followed by the halfyear number, eg. H20081.
        """
        y = int(tag[1:5])
        h = int(tag[5])
        return cls(year=y, halfyear=h)

    def idtag(self):
        """halfyear tags have the upper-case letter H + the four digit year,
           followed by the halfyear number, eg. H20081.
        """
        return f'H{self.year}{self.halfyear}'

    def __add__(self, n):
        """Add n halfyears to self.
        """
        return Halfyear(self.year, self.halfyear + n)

    def __radd__(self, n):
        return self + n

    def __sub__(self, n):
        return self + (-n)

    # rsub doesn't make sense

    def prev(self):
        """Previous halfyear.
        """
        return self - 1

    def next(self):
        """Next halfyear.
        """
        return self + 1

    def __hash__(self):
        return self.halfyear

    def dayiter(self):
        """Yield all days in all months in halfyear.
        """
        for m in self.months:
            yield from m.days()

    def _format(self, fmtchars):
        # http://blog.tkbe.org/archive/date-filter-cheat-sheet/
        for ch in fmtchars:
            if ch == 'H':
                yield str(self.halfyear)
            else:
                yield ch

    def format(self, fmt=None):
        """Format according to format string. Default format is
           four-digit-year and halfyear-number.
        """
        if fmt is None:
            fmt = "H"
        tmp = list(self._format(list(fmt)))
        return ''.join(tmp)
