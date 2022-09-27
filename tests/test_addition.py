import ttcal


def test_repr():
    assert repr(ttcal.Period(months=1)) == "Period(1 months)"
    assert repr(ttcal.Period(months=13)) == "Period(1 years, 1 months)"
    assert repr(ttcal.Period(years=1, months=1)) == "Period(1 years, 1 months)"


def test_period_cmp():
    assert ttcal.Period(months=5) == ttcal.Period(months=5)
    assert not ttcal.Period(months=5) == ttcal.Period(months=4)
    assert ttcal.Period(months=4) != ttcal.Period(months=5)
    assert ttcal.Period(months=4) < ttcal.Period(months=5)
    assert ttcal.Period(months=4) <= ttcal.Period(months=5)
    assert ttcal.Period(months=5) > ttcal.Period(months=4)
    assert ttcal.Period(months=5) >= ttcal.Period(months=4)


def test_period_add():
    print("1m =", ttcal.Period(months=1))
    print("1m + 1m =", ttcal.Period(months=1) + ttcal.Period(months=1))
    assert ttcal.Period(months=1) + ttcal.Period(months=1) == ttcal.Period(months=2)


def test_add_month():
    assert ttcal.Day(2020, 1, 30) + ttcal.Period(months=1) == ttcal.Day(2020, 2, 29)
    assert ttcal.Day(2020, 1, 30) + ttcal.Period(months=2) == ttcal.Day(2020, 3, 30)
    assert ttcal.Day(2020, 1, 30) + ttcal.Period(months=3) == ttcal.Day(2020, 4, 30)
    assert ttcal.Day(2020, 1, 30) + ttcal.Period(months=4) == ttcal.Day(2020, 5, 30)
    assert ttcal.Day(2020, 1, 30) + ttcal.Period(months=5) == ttcal.Day(2020, 6, 30)


def test_add_year_leap():
    assert ttcal.Day(2020, 2, 29) + ttcal.Period(years=1) == ttcal.Day(2021, 2, 28)
    assert ttcal.Day(2020, 2, 29) + ttcal.Period(years=2) == ttcal.Day(2022, 2, 28)
    assert ttcal.Day(2020, 2, 29) + ttcal.Period(years=3) == ttcal.Day(2023, 2, 28)
    assert ttcal.Day(2020, 2, 29) + ttcal.Period(years=4) == ttcal.Day(2024, 2, 29)
    assert ttcal.Day(2020, 2, 29) + ttcal.Period(years=5) == ttcal.Day(2025, 2, 28)


def test_add_month_lastday():
    jan1 = ttcal.Day(2020, 1, 1)
    jan31 = ttcal.Day(2020, 1, 31)
    feb29 = ttcal.Day(2020, 2, 29)
    months1 = ttcal.Period(months=1)
    months2 = ttcal.Period(months=2)
    months3 = ttcal.Period(months=3)
    months4 = ttcal.Period(months=4)
    months5 = ttcal.Period(months=5)
    years1 = ttcal.Period(years=1)

    print("jan1 + 1month=", jan1 + months1)
    assert jan1 + months1 == ttcal.Day(2020, 2, 1)
    assert feb29 + years1 == ttcal.Day(2021, 2, 28)
    assert feb29 + months1 == ttcal.Day(2020, 3, 29)
    assert jan31 + months1 == feb29
    assert jan31 + months2 == ttcal.Day(2020, 3, 31)
    assert jan31 + months3 == ttcal.Day(2020, 4, 30)
    assert jan31 + months4 == ttcal.Day(2020, 5, 31)
    assert jan31 + months5 == ttcal.Day(2020, 6, 30)
    assert jan31 - months1 == ttcal.Day(2019, 12, 31)

    # assert ttcal.Period(months=1) + ttcal.Period(months=1) == ttcal.Period(months=2)

    print("feb29 + months1 + months1 = ", feb29 + (months1 + months1))
    assert feb29 + (months1 + months1) == ttcal.Day(2020, 4, 29)

    print("(d + 1m) + 1m =", (feb29 + months1) + months1)
    assert feb29 + months1 == ttcal.Day(2020, 3, 29)
    assert (feb29 + months1) + months1 == ttcal.Day(2020, 4, 29)
