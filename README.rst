

ttcal - calendar operations
===========================

This is a small library for calendar operations.

Usage::

    >>> from ttcal import *
    >>> Today()
    2023-7-2-7
    >>> Today() + 1
    2023-7-3-7
    >>> import datetime
    >>> isinstance(Today(), datetime.date)
    True
    >>> Day(1991, 2, 20)
    1991-2-20-2
    >>> Month()
    Month(2023, 7)
    >>> Month() + 2
    Month(2023, 9)
    >>> Year()
    Year(2023)
    >>> Year() + 2
    Year(2025)
    >>> Day(2024, 2, 29)
    2024-2-29-2
    >>> Day(2024, 2, 29) + Period(months=2)
    2024-4-29-4
    >>> Day(2024, 4, 30) - Period(months=2)
    2024-2-29-2
    >>>


