"""
Date (single day) operations.
"""
import calendar
import datetime
import re
from typing import List, Tuple
from .calfns import rangecmp, rangetuple
from .duration import Duration, Period


class fstr(str):
    """String sub-class with a split() method that splits a given indexes.

       Usage::
          >>> r = fstr('D2008022002')
          >>> print(r.split(1, 5, 7, 9))
          ['D', '2008', '02', '20', '02']
          >>> _, year, _ = r.split(1,5)
          >>> year
          '2008'

    """
    def _validate_indexes(self, *ndxs: Tuple[int]) -> Tuple[int]:
        """Return indexes that are valid for this string, in order.
        """
        ndxs = sorted(set(ndxs))
        if not ndxs:
            return []
        if ndxs and ndxs[0] == 0:
            ndxs = ndxs[1:]
        while ndxs and ndxs[-1] > len(self):
            ndxs = ndxs[:-1]
        return ndxs

    def split(self, *ndxs: Tuple[int]) -> List[str]:
        ndxs = self._validate_indexes(*ndxs)
        if not ndxs:
            return [self]

        res = []
        b = 0
        while ndxs:
            a, b, ndxs = b, ndxs[0], ndxs[1:]
            res.append(self[a:b])
        res.append(self[b:])

        return res

    @classmethod
    def join(cls, strings: List[str], *ndxs: Tuple[int]) -> str:
        ndxs = [n for n in ndxs if n > 0]
        if not ndxs:
            return strings[0] if strings else ''
        res = ''
        for s, n in zip(strings, ndxs):
            res += s[:n]
        res += strings[-1]
        return res


def fsplit(strval: str, *ndxs: Tuple[int]) -> List[str]:
    """Split a string at given indexes.
    """
    return fstr(strval).split(*ndxs)


def fjoin(strings: List[str], *ndxs: Tuple[int]) -> str:
    """Join a sequence of strings.
    """
    return fstr.join(strings, *ndxs)


class Day(datetime.date):  # pylint:disable=too-many-public-methods
    """A calendar date.
    """

    day_name = '''mandag tirsdag onsdag torsdag fredag
                  lørdag søndag'''.split()

    day_code = "M U W H F A S".split()

    def __reduce__(self):
        """Support for pickling Day objects.

           Returns a tuple for reconstructing the Day instance.
        """
        return Day, (self.year, self.month, self.day)

    def __int__(self):
        """Convert Day to integer (ordinal) representation.
        """
        return self.toordinal()

    @classmethod
    def from_idtag(cls, tag):
        """Return Day from idtag.

           An idtag is a string representation used for serialization.
           Format: 'd' followed by YYYYMMDDBB where BB is membermonth.

           Example: 'd2008022002' represents Feb 20, 2008 in member month 2.
        """
        if len(tag) == 9:
            # d2008022002
            y, m, d = map(int, fstr(tag).split(1, 5, 7)[1:])
            return cls(y, m, d, membermonth=m)

        # d2008022002
        y, m, d, b = map(int, fstr(tag).split(1, 5, 7, 9)[1:])
        return cls(y, m, d, membermonth=b)

    @classmethod
    def parse(cls, strval):
        """Parse date value from a string.  Allowed syntax include
           ::

               yyyy-mm-dd, yyyy-m-dd, yyyy-mm-d, yyyy-m-d
               dd-mm-yyyy, etc.
               dd/mm/yyyy, ...
               dd.mm.yyyy, ...
               ddmmyyyy

        """
        if not strval or not strval.strip():
            # strval is None or contains only spaces
            return None

        datere = re.compile(r"""
            (?:\s*)
            (?P<isodate>
              (?P<iso_yr>[12]\d{3})
              (?P<sep>[-./\s])
              (?P<iso_mnth>0[1-9]|1[012]|[1-9])
              (?P=sep)
              (?P<iso_day>3[01]|[12]\d|0[1-9]|[1-9]))
            |(?P<dmy>
              (?P<dmy_day>3[01]|[12]\d|0[1-9]|\d)
              (?P<dmy_sep>[-./\s])
              (?P<dmy_mnth>0[1-9]|1[012]|\d)
              (?P=dmy_sep)
              (?P<dmy_yr>[12]\d{3}))
            |(?P<nsp>
              (?P<nsp_day>3[01]|[12]\d|0[1-9])
              (?P<nsp_mnth>0[1-9]|1[012])
              (?P<nsp_yr>[12]\d{3}))
            |(?P<isonsp>
              (?P<isonsp_yr>20[1-5]\d)
              (?P<isonsp_mnth>0[1-9]|1[012])
              (?P<isonsp_day>3[01]|[12]\d|0[1-9]))
            |(?P<two>
              (?P<two_day>3[01]|[12]\d|0[1-9]|\d)
              (?P<two_sep>[./\s])
              (?P<two_mnth>0[1-9]|1[012]|\d)
              (?P=two_sep)
              (?P<two_yr>[1-9]\d))
            (?:\s*)
        """, re.VERBOSE)
        m = datere.match(strval)
        if not m:
            raise ValueError(f"Cannot parse {strval!r} as date.")
        prefix = ''

        g = m.groupdict()
        if g['isodate']:
            prefix = 'iso'

        elif g['dmy']:
            prefix = 'dmy'

        elif g['nsp']:
            prefix = 'nsp'

        elif g['isonsp']:
            prefix = 'isonsp'

        elif g['two']:
            prefix = 'two'

        day, month, year = (int(g[f'{prefix}_{val}'])
                            for val in ['day', 'mnth', 'yr'])

        if year < 13:
            raise ValueError(f"Cannot parse {strval!r} as date.")
        if year < 100:
            year += 2000

        return cls(year, month, day)

    def __new__(cls, *args, **kw):
        """Create a new Day instance.

           Args can be (year, month, day), a single date/Day object, or empty
           for today. Supports optional membermonth keyword argument for
           specifying which month this day belongs to (for week calculations).
        """
        if len(args) == 3:
            y, m, d = args
        elif len(args) == 1:
            t = args[0]
            y, m, d = t.year, t.month, t.day
        elif len(args) == 0:
            t = datetime.date.today()
            y, m, d = t.year, t.month, t.day
        else:
            raise TypeError('incorrect number of arguments')

        obj = super().__new__(cls, y, m, d)
        obj.membermonth = kw.get('membermonth', obj.month)
        return obj

    @staticmethod
    def get_day_name(daynum, length=None):
        """Return dayname for daynum.

           Args:
               daynum: Day number (0=Monday through 6=Sunday)
               length: Optional max length to truncate the name

           Returns: Norwegian day name as a string.
        """
        if length is None:
            return Day.day_name[daynum]
        return Day.day_name[daynum][:length]

    def range(self):
        """Return an iterator for the range of `self`.
        """
        return Days(self.first, self.last)

    def rangetuple(self):
        """Return a datetime tuple representing this day
           (as a half-open interval).
        """
        return self.datetime(), (self + 1).datetime()

    def between_tuple(self):
        """Return a tuple of datetimes that is convenient for sql
           `between` queries.
        """
        return (self.first.datetime(),
                (self.last + 1).datetime() - datetime.timedelta(seconds=1))

    @property
    def middle(self):
        """Return the day that splits the date range in half.
        """
        middle = (self.first.toordinal() + self.last.toordinal()) // 2
        return Day.fromordinal(middle)

    def __hash__(self):
        """Return hash value for Day objects.
        """
        return hash(f'{self.year:04}{self.month:02}{self.day:02}')

    def __repr__(self):
        """Return the string representation of the Day object.
        """
        return f'{self.year}-{self.month}-{self.day}-{self.membermonth}'

    def __str__(self):
        """Return a formatted string representation in ISO format.
        """
        return f'{self.year:04}-{self.month:02}-{self.day:02}'

    def datetime(self, hour=0, minute=0, second=0):
        """Extend `self` to datetime.

           Args:
               hour: Hour value (0-23), defaults to 0
               minute: Minute value (0-59), defaults to 0
               second: Second value (0-59), defaults to 0

           Returns: A datetime.datetime object for this day at the specified time.
        """
        return datetime.datetime(self.year, self.month, self.day,
                                 hour, minute, second)

    def date(self):
        """Explicitly convert to datetime.date.

           Returns a standard Python datetime.date object equivalent to this Day.
        """
        return datetime.date(self.year, self.month, self.day)

    def datetuple(self):
        """Return year, month, day.

           Useful for unpacking or passing to functions that expect
           separate year, month, and day arguments.
        """
        return self.year, self.month, self.day

    def __add__(self, n):
        """Add days or a Period to this Day.

           Args:
               n: Integer number of days to add, or a Period object

           Returns: A new Day object offset by the specified amount.
        """
        if isinstance(n, Period):
            return n.add_to_day(Day, self)
        return Day.fromordinal(self.toordinal() + n)

    # make first and last properties, because
    # self.first = self.last = self creates too many cycles :-)
    @property
    def first(self):
        """Define self == self.first for polymorphic usage with other classes.
        """
        return self

    @property
    def last(self):
        """Define self == self.last for polymorphic usage with other classes.
        """
        return self

    def next(self):
        """Return Tomorrow (for use in templates).
        """
        return self + 1

    def prev(self):
        """Return Yesterday (for use in templates).
        """
        return self - 1

    def __sub__(self, x):
        """Return number of days between Days or Day n days ago.

           Args:
               x: Can be a Day (returns int difference), Period, Duration,
                  or int (returns new Day)

           Returns: Integer days between two Days, or a new Day object offset
                   by the specified amount.

           Raises: ValueError if x is not a supported type.
        """
        if isinstance(x, Day):
            return self.toordinal() - x.toordinal()
        if isinstance(x, Period):
            return x.sub_from_day(Day, self)
        if isinstance(x, Duration):
            return Day.fromordinal(self.toordinal() - x.days)
        if isinstance(x, int):
            return Day.fromordinal(self.toordinal() - x)

        raise ValueError(
            f'Wrong operands for subtraction: {type(self)} and {type(x)}')

    @property
    def dayname(self):
        """The semi-localized name of self.
        """
        return self.day_name[self.weekday]

    @property
    def code(self):
        """One letter code representing the dayname.
        """
        return self.day_code[self.weekday]

    @property
    def weeknum(self):
        """Return the isoweek of `self`.
        """
        return self.isocalendar()[1]

    @property
    def isoyear(self):
        """Return the `isoyear` of `self`.
        """
        return self.isocalendar()[0]

    # week, Month, and Year, are added later (don't uncomment them here, since
    # that leads to nasty circular dependencies.
    #
    # @property
    # def week(self):
    #     """Return a Week object representing the week `self` belongs to.
    #     """
    #     from .week import Week
    #     return Week.weeknum(self.weeknum, self.isoyear)

    # @property
    # def Month(self):
    #     """Return a Month object representing the month `self` belongs to.
    #     """
    #     from .month import Month
    #     return Month(self.year, self.month)

    # @property
    # def Year(self):
    #     """Return a Year object representing the year `self` belongs to.
    #     """
    #     from .year import Year
    #     return Year(self.year)

    @property
    def display(self):
        """Return the 'class' of self.
        """
        res = set()
        if self.today and (self.membermonth == self.month):
            res.add('today')
        if self.in_month:
            res.add('month')
        else:
            res.add('noday')
        if self.weekend:
            res.add('weekend')
        if hasattr(self, 'mark'):
            res.add(self.mark)

        return ' '.join(res)

    @property
    def idtag(self):
        """Return the idtag for `self`: dyyyymmddmm.
        """
        return f'd{self.year}{self.month:02d}{self.day:02d}{self.membermonth:02d}'

    @property
    def today(self):  # pylint:disable=arguments-differ,invalid-overridden-method
        """True if self is today.
        """
        return self.compare(datetime.date.today()) == 'day'

    @property
    def weekday(self):  # pylint:disable=invalid-overridden-method
        """True if self is a weekday.
        """
        return calendar.weekday(self.year, self.month, self.day)

    @property
    def weekend(self):
        """True if self is Saturday or Sunday.
        """
        return 5 <= self.weekday <= 6

    @property
    def special(self):  # pylint:disable=no-self-use
        """True if the database has an entry for this date (sets special_hours).
        """
        return False

    @property
    def in_month(self):
        """True iff the day is in its month.
        """
        return self.month == self.membermonth

    def compare(self, other):
        """Return how similar self is to other, i.e. the smallest factor
           they have in common ('day', 'month', or 'year').
           Returns None if the Days are in different years.
        """
        if not hasattr(other, 'year'):
            return None
        if self.year == other.year:
            if self.month == other.month:
                if self.day == other.day:
                    return 'day'
                return 'month'
            return 'year'
        return None

    def _format(self, fmtchars):
        """Map single char format codes to values.

           Internal method that maps format characters to their corresponding
           values for custom date formatting.
        """
        # http://blog.tkbe.org/archive/date-filter-cheat-sheet/
        simplefmt = {
            'y': lambda: str(self.year)[-2:],
            'Y': lambda: str(self.year),
            'W': lambda: str(self.weeknum),
            'w': lambda: str(self.weekday),
            'n': lambda: str(self.month),
            'm': lambda: f'{int(self.month):02}',
            'b': lambda: self.Month.format('b'),
            'M': lambda: self.Month.format('M'),
            'N': lambda: self.Month.format('N'),
            'F': lambda: self.Month.format('F'),
            'j': lambda: str(self.day),
            'd': lambda: f'{int(self.day):02}',
            'D': lambda: self.dayname[:3],
            'l': lambda: self.dayname,
            'z': lambda: str(int(self) - int(Day(self.year, 1, 1))),
        }
        ch = ""
        for ch in fmtchars:
            yield simplefmt.get(ch, lambda ch=ch: ch)()

    def format(self, fmt=None):
        """Emulate Django's date filter.

           Args:
               fmt: Format string using Django date filter codes.
                   If None, uses 'j. F Y' as default.

           Returns: Formatted date string according to the format specification.
        """
        if fmt is None:
            # pylint:disable=C0301
            # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-DATE_FORMAT
            fmt = "N j, Y"
        tmp = list(self._format(list(fmt)))
        return ''.join(tmp)

    def timetuple(self):
        """Create timetuple from datetuple.
           (to interact with datetime objects).
        """
        d = datetime.date(*self.datetuple())
        t = datetime.time()
        return datetime.datetime.combine(d, t)

    def __lt__(self, other):
        """Less than comparison using range semantics.
        """
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) < 0

    def __le__(self, other):
        """Less than or equal comparison using range semantics.
        """
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) <= 0

    def __eq__(self, other):
        """Equal comparison using range semantics (overlapping ranges).
        """
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) == 0

    def __gt__(self, other):
        """Greater than comparison using range semantics.
        """
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) > 0

    def __ge__(self, other):
        """Greater than or equal comparison using range semantics.
        """
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) >= 0


class Today(Day):
    """Special subclass for today's date.

       Always represents the current date regardless of construction arguments.
       Has a special 'today' attribute set to True for template checking.
    """
    def __new__(cls, *args, **kw):
        """Create a Today instance for the current date.

           Ignores all arguments and always returns today's date.
        """
        t = datetime.date.today()
        y, m, d = t.year, t.month, t.day
        obj = super().__new__(cls, y, m, d)
        obj.membermonth = obj.month
        return obj

    today = True


class Days(list):
    """A contiguous set of days.

       Represents a range of consecutive days as a list, with convenience
       methods for accessing first/last days and range operations.
    """
    def __init__(self, start, end, start_week=False):
        """Initialize a Days object with a range of days.

           Args:
               start: The first Day in the range
               end: The last Day in the range
               start_week: If True, adjust start to beginning of week (Monday)
        """
        super().__init__()
        assert start <= end
        if start_week:
            start = start - start.weekday  # set to monday

        for i in range(start.toordinal(), end.toordinal() + 1):
            self.append(Day.fromordinal(i))

    @property
    def first(self):
        """Return the first day in the range.
        """
        return self[0]

    @property
    def last(self):
        """Return the last day in the range.
        """
        return self[-1]

    def range(self):
        """Return an iterator for the range of `self`.
        """
        return Days(self.first, self.last)

    def between_tuple(self):
        """Return a tuple of datetimes that is convenient for sql
           `between` queries.
        """
        return (self.first.datetime(),
                (self.last + 1).datetime() - datetime.timedelta(seconds=1))

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
