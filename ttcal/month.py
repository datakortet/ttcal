"""
Month operations.
"""
from __future__ import annotations
from typing import Optional, List, Tuple, Union, Iterator, Any, ClassVar, TYPE_CHECKING
import re
import calendar
import datetime

if TYPE_CHECKING:
    from .year import Year

from .day import Day, Days
from .week import Week
from .calfns import chop, rangecmp, rangetuple


class Month:  # pylint:disable=too-many-public-methods
    """A calendar month.
    """

    month_name: ClassVar[List[str]] = [
        '', 'Januar', 'Februar', 'Mars', 'April', 'Mai', 'Juni', 'Juli',
        'August', 'September', 'Oktober', 'November', 'Desember'
    ]
    year: Optional[int] = None
    month: Optional[int] = None
    calendar: calendar.Calendar
    name: str
    short_name: str
    weeks: List[Week]

    @classmethod
    def from_idtag(cls, tag: str) -> Month:
        """Parse idtag into `class`:Month.

           An idtag is a string representation used for serialization.
           Format: 'm' followed by YYYYMM (year and month).

           Example: 'm200802' represents February 2008.
        """
        # m20082
        y = int(tag[1:5])
        m = int(tag[5:])
        return cls(year=y, month=m)

    @classmethod
    def from_date(cls, d: Union[datetime.date, Day]) -> Month:
        """Create a Month from the date ``d``.
        """
        return cls(year=d.year, month=d.month)

    def rangetuple(self) -> Tuple[datetime.datetime, datetime.datetime]:
        """Return a datetime tuple representing this month
           (as a half-open interval).
        """
        return self.first.datetime(), (self.last + 1).datetime()

    @classmethod
    def parse(cls, txt: Optional[str]) -> Optional[Month]:
        """Parse a textual representation into a Month object.
           Format YYYY-MM?
        """
        if not txt:
            return None

        mnth_matcher = re.compile(
            r"""
            (?P<year>\d{4})-?(?P<month>\d{1,2})
            """, re.VERBOSE)
        m = mnth_matcher.match(txt)
        if not m:
            msg = f"Ugyldig format, må være åååå-mm, ikke {txt!r}."
            raise ValueError(msg)
        mnth_groups = m.groupdict()

        return cls(int(mnth_groups["year"]), int(mnth_groups["month"]))

    def __init__(self, year: Optional[int] = None, month: Optional[int] = None,
                 date: Optional[datetime.date] = None) -> None:
        """Initialize a Month object.

           Args:
               year: The year (e.g., 2024)
               month: The month number (1-12)
               date: Optional date object to extract year/month from

           If no arguments provided, defaults to current month.
           Raises ValueError if month is not in range 1-12.
        """
        super().__init__()
        if date is not None:
            self.year = date.year
            self.month = date.month
        elif year is month is date is None:
            td = datetime.date.today()
            self.year = td.year
            self.month = td.month
        else:
            assert None not in (year, month)
            self.year = year
            self.month = month

        if not 1 <= self.month <= 12:
            raise ValueError("Month must be in 1..12.")

        self.calendar = calendar.Calendar()
        self.name = self.month_name[self.month]
        self.short_name = self.name[:3]
        # self.short_name = calendar.month_abbr[self.month]
        self.weeks = [Week(days, self.month) for days in self._weeks()]
        # self.day = 1

    def __call__(self, daynum: Optional[int] = None) -> Union[Month, Day]:
        """Return the given Day for this month.

           Args:
               daynum: Day number in the month (1-31). If None, returns self.

           Returns: A Day object for the specified day, or self if no day provided.

           Usage::

               month = ttcal.Month(2024, 12)
               christmas = month(25)  # Returns Day for Dec 25, 2024
        """
        if daynum is None:  # pragma: nocover
            return self  # for when django tries to do value = value() *sigh*
        return Day(self.year, self.month, daynum)

    def __reduce__(self) -> Tuple[type, Tuple[int, int]]:
        """Deepcopy helper.

           Returns a tuple for reconstructing the Month instance during
           pickling/deepcopy operations.
        """
        return Month, (self.year, self.month)

    def __str__(self) -> str:  # pragma: nocover
        """Return string representation in YYYY-MM format.
        """
        return f'{int(self.year):04}-{int(self.month):02}'

    def __repr__(self) -> str:
        """Return string representation for debugging.
        """
        return f'Month({self.year}, {self.month})'

    # @property
    # def Year(self):
    #     """Return a Year object for the year-part of this month.
    #     """
    #     return Year(self.year)

    @property
    def Month(self) -> Month:
        """Return the month (for api completeness).
        """
        return self

    def __hash__(self) -> int:
        """Return hash value for Month objects.
        """
        return self.year * 100 + self.month

    # def __eq__(self, other):
    #     noinspection PyBroadException
    # try:
    #     return self.year == other.year and self.month == other.month
    # except:
    #     return False

    def __len__(self) -> int:
        """Return the number of days in this month.
        """
        _, n = calendar.monthrange(self.year, self.month)
        return n

    def datetuple(self) -> Tuple[int, int, int]:
        """First date in month.
        """
        return self.year, self.month, 1

    def __lt__(self, other: Any) -> bool:
        """Less than comparison using range semantics.
           Integers are compared against the month number (1-12).
        """
        if isinstance(other, int):
            return self.month < other
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) < 0

    def __le__(self, other: Any) -> bool:
        """Less than or equal comparison using range semantics.
           Integers are compared against the month number (1-12).
        """
        if isinstance(other, int):
            return self.month <= other
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) <= 0

    def __eq__(self, other: Any) -> bool:
        """Equal comparison using range semantics (overlapping ranges).
           Integers are compared against the month number (1-12).
        """
        if isinstance(other, int):
            return self.month == other
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) == 0

    def __ne__(self, other: Any) -> bool:
        """Not equal comparison.
        """
        return not self == other

    def __gt__(self, other: Any) -> bool:
        """Greater than comparison using range semantics.
           Integers are compared against the month number (1-12).
        """
        if isinstance(other, int):
            return self.month > other
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) > 0

    def __ge__(self, other: Any) -> bool:
        """Greater than or equal comparison using range semantics.
           Integers are compared against the month number (1-12).
        """
        if isinstance(other, int):
            return self.month >= other
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) >= 0

    def numdays(self) -> int:  # for use in template
        """The number of days in the month.
        """
        return len(self)

    def __add__(self, n: int) -> Month:
        """Add n months to self.
        """
        me = self.year * 12 + (self.month - 1)
        me += n
        q, r = divmod(me, 12)
        return Month(q, r + 1)

    def __radd__(self, n: int) -> Month:
        """Add n months to self (right addition).
        """
        return self + n

    def __sub__(self, n: Union[int, Month]) -> Union[int, Month]:
        """Subtract months or get difference between months.

           Args:
               n: Either an int (months to subtract) or Month (to get difference)

           Returns: A new Month if n is int, or int difference if n is Month.
        """
        if isinstance(n, Month):
            first, last = min(self, n), max(self, n)
            ydiff = last.year - first.year
            mdiff = last.month - first.month
            res = 12*ydiff + mdiff
            if self > n:
                return res
            return -res
        return self + (-n)

    # rsub doesn't make sense

    # NOTE: Django's query engine calls both __call__ and __iter__ on values
    #       that are passed in, and uses the return values instead of the value
    #       itself (i.e. with the implementation below, the queryset would get
    #       a list of Week objects instead of a Month object).
    # NB: W:\srv\venv\dev\Lib\site-packages\django\db\models\sql\where.py
    # NB: temp comment
    # NB:  if is_iterator(value):
    # NB:        # Consume any generators immediately, so that we can determine
    # NB:        # emptiness and transform any non-empty values correctly.
    # NB:        value = list(value)
    # def __iter__(self):
    #     return iter(self.weeks)

    def dayiter(self) -> Iterator[Day]:
        """Iterator over days in each week of month.
        """
        for wk in iter(self.weeks):
            yield from wk

    def days(self) -> List[Day]:
        """Return a list of days (`class`:ttcal.Day) in this month.
        """
        res: List[Day] = []
        for wk in iter(self.weeks):
            for day in wk:
                if day.month == self.month:
                    res.append(day)  # yield day
        return res

    def idtag(self) -> str:
        """Return a text representation that is parsable by the from_idtag
           function (above), and is useable as part of an url.
        """
        return f'm{int(self.year)}{int(self.month)}'

    @property
    def daycount(self) -> int:
        """The number of days in this month (as an int).
        """
        n = calendar.mdays[self.month]
        if self.month == 2 and calendar.isleap(self.year):
            n += 1
        return n

    def prev(self) -> Month:
        """Previous month.
        """
        return self - 1

    def next(self) -> Month:
        """Next month.
        """
        return self + 1

    @property
    def first(self) -> Day:
        """First day in month.
        """
        return Day(self.year, self.month, 1)

    @property
    def last(self) -> Day:
        """Last day in month.
        """
        return Day(self.year, self.month, self.daycount)

    def _weeks(self) -> Iterator[List[datetime.date]]:
        """Generate week-long lists of dates for this month.

           Used internally to construct the weeks attribute.
        """
        c = self.calendar
        return chop(c.itermonthdates(self.year, self.month), 7)

    def __contains__(self, date: Any) -> bool:
        """Check if a date is in this month.
        """
        return self.year == date.year and self.month == date.month

    def __getitem__(self, day: Day) -> Day:
        """Get a specific day from the month by index.
        """
        for wk in self.weeks:
            for d in wk:
                if d.compare(day) == 'day':
                    return d
        raise KeyError

    def mark(self, d: Day, value: str = 'mark', method: str = 'replace') -> None:
        """Add a 'mark' to a day in this month.
        """
        try:
            day = self[d]
            if method == 'replace':
                day.mark = value
            elif method == 'append':
                if hasattr(day, 'mark'):
                    day.mark += value
                else:
                    day.mark = value
            else:  # pragma: nocover
                pass

        except KeyError:  # pragma:nocover
            pass

    def marked_days(self) -> Iterator[Day]:
        """Yield all days with marks.
        """
        for wk in self.weeks:
            for d in wk:
                if hasattr(d, 'mark'):
                    yield d

    def _format(self, fmtchars: List[str]) -> Iterator[str]:
        """Map single char format codes to values.

           Internal method that maps format characters to their corresponding
           values for custom month formatting.
        """
        # http://blog.tkbe.org/archive/date-filter-cheat-sheet/
        for ch in fmtchars:
            if ch == 'y':
                yield str(self.year)[-2:]
            elif ch == 'Y':
                yield str(self.year)
            elif ch == 'n':
                yield str(self.month)
            elif ch == 'm':
                yield f'{self.month:02}'
            elif ch == 'b':
                yield self.name[:3].lower()
            elif ch == 'M':
                yield self.name[:3]
            elif ch == 'N':
                # should be AP style, but doesn't make sense outside US.
                yield self.name[:3]
            elif ch == 'F':
                yield self.name
            else:
                yield ch

    def format(self, fmt: Optional[str] = None) -> str:
        """Format according to format string. Default format is
           monthname, four-digit-year.
        """
        if fmt is None:
            fmt = "F, Y"
        tmp = list(self._format(list(fmt)))
        return ''.join(tmp)

    def range(self) -> Days:
        """Return an iterator for the range of `self`.
        """
        # if hasattr(self, 'dayiter'):
        #     return self.dayiter()
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

    def timetuple(self) -> datetime.datetime:
        """Create timetuple from datetuple.
           (to interact with datetime objects).
        """
        d = datetime.date(*self.datetuple())
        t = datetime.time()
        return datetime.datetime.combine(d, t)


# noinspection PyPep8Naming
def _Month(self: Day) -> Month:
    """Return a Month object representing the month `self` belongs to.
    """
    return Month(self.year, self.month)


Day.Month = property(_Month)
