# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`ttcal` is a Python library for calendar operations, providing classes for working with Days, Weeks, Months, Quarters, Years, and time Durations/Periods. The library extends Python's standard `datetime` module with more semantic and intuitive calendar manipulation.

## Common Usage Examples

```python
from ttcal import *

# Creating calendar objects
today = Today()
day = Day(2024, 2, 29)
month = Month(2024, 2)
year = Year(2024)
week = Week.weeknum(15, 2024)
quarter = Quarter(2024, 1)

# Arithmetic operations
day + 7                    # Add 7 days
day + Period(months=2)     # Smart month addition (handles month-end dates)
month + 3                  # Add 3 months
year + 1                   # Add 1 year

# Parsing from strings
Day.parse("2024-02-29")    # ISO format
Day.parse("29/02/2024")    # DMY format
Month.parse("2024-02")     # Year-month format
Duration.parse("2:30:00")  # HH:MM:SS format

# Range operations
month.first                # First day of month
month.last                 # Last day of month
month.rangetuple()         # (datetime_start, datetime_end) half-open interval
month.between_tuple()      # For SQL BETWEEN queries

# Accessing year components
year.Q1                    # First quarter (list of 3 months)
year.january               # January month object
year.december(25)          # Day(year, 12, 25)
```

## Core Architecture

### Main Calendar Classes

The library is built around five primary calendar classes, all located in `ttcal/`:

- **Day** (`day.py`) - Extends `datetime.date` with calendar-aware operations. Days have a `membermonth` attribute tracking which month display they belong to (important for calendar rendering).
- **Week** (`week.py`) - Represents ISO weeks. Weeks belong to ISO years (not calendar years).
- **Month** (`month.py`) - Represents calendar months containing weeks.
- **Quarter** (`quarter.py`) - Represents fiscal quarters (3-month periods).
- **Year** (`year.py`) - Represents calendar years containing months. Includes convenient properties like `.Q1`-`.Q4` for quarters, `.H1`-`.H2` for halves, and `.january`-`.december` for month access.
- **Days** (`day.py`) - A list subclass representing contiguous day ranges. Supports `.first`, `.last`, `.middle` properties and range operations like other calendar objects.

### Critical Design Patterns

1. **Circular Dependencies**: Classes have mutual dependencies resolved by late property binding:
   - `Day.Month`, `Day.Year`, and `Day.week` are added as properties from their respective modules
   - See bottom of `month.py`, `year.py`, and `week.py` for these property definitions

2. **Range Semantics**: All calendar objects support:
   - `.first` and `.last` properties returning Day objects
   - `.rangetuple()` returning half-open datetime intervals `[start, end)`
   - `.between_tuple()` returning closed intervals for SQL BETWEEN queries
   - `.middle` property returning the midpoint Day
   - Comparison operators using interval semantics (overlap = equality)

3. **idtag System**: Each class has serializable string identifiers:
   - Day: `d{year}{month:02d}{day:02d}{membermonth:02d}` (e.g., `d2023070207`)
   - Week: `w{isoyear}{weeknum}` (e.g., `w202301`)
   - Month: `m{year}{month}` (e.g., `m20237`)
   - Quarter: `q{year}{quarter}` (e.g., `q20231`)
   - Year: `y{year}` (e.g., `y2023`)
   - Use `.from_idtag(tag)` class methods to deserialize
   - Use top-level `from_idtag(tag)` function in `__init__.py` to automatically detect and deserialize any idtag type

4. **Duration vs Period**:
   - **Duration** (`duration.py`) - Fixed timedelta (days, hours, minutes). Can be parsed from strings like "2d 3:30:00"
   - **Period** (`duration.py`) - Semantic months/years (variable length due to month/year variability)
   - Day arithmetic: `Day + int` adds days, `Day + Period` adds months/years intelligently
   - Period handles month-end edge cases smartly: `Day(2024, 1, 31) + Period(months=1)` → `Day(2024, 2, 29)` (clamps to last day of month)

5. **Parsing Methods**: Multiple classes support flexible parsing from strings:
   - `Day.parse(strval)` - Accepts ISO (yyyy-mm-dd), DMY (dd/mm/yyyy), compact (ddmmyyyy), and more
   - `Month.parse(txt)` - Accepts "YYYY-MM" or "YYYYMM" formats
   - `Duration.parse(txt)` - Accepts "HHH:MM:SS", "Nd HH:MM:SS", "-2d 3:30:00", etc.

6. **Format System**: All calendar classes have `.format(fmt)` methods using Django-style format codes:
   - Day: `d.format("Y-m-d")` → "2024-02-29"
   - Month: `m.format("F Y")` → "Februar 2024"
   - Year: `y.format("Y")` → "2024"

### Helper Functions

`calfns.py` contains:
- `chop(iterator, n)` - Split iterator into n-sized chunks
- `isoweek(year, week)` - Generate days in an ISO week
- `rangetuple(x)` - Convert objects to datetime ranges
- `rangecmp(interval_a, interval_b)` - Compare intervals with overlap semantics

### String Splitting Utilities

`day.py` includes `fstr` class with positional splitting:
- `fstr('d2008022002').split(1, 5, 7, 9)` → `['d', '2008', '02', '20', '02']`
- Used extensively in idtag parsing

## Development Commands

### Testing
```bash
# Run all tests with coverage
workon ttcal311 && pytest -vv --cov=ttcal tests

# Run specific test file
workon ttcal311 && pytest tests/test_ttcal_day.py -v

# Run single test
workon ttcal311 && pytest tests/test_ttcal_day.py::test_function_name -v
```

### Linting
```bash
# Flake8 (used in CI)
flake8 ttcal/** --max-line-length=199

# pep8 via dk (custom build tool from dktasklib/dkbuild.yml)
dk pep8

# pylint via dk
dk pylint
```

### Building
```bash
# Build distribution packages
python setup.py sdist bdist_wheel
```

### Task Runner
The project uses `invoke` with `dktasklib`:
```bash
# Available tasks in tasks.py
invoke version      # Show version
invoke upversion    # Increment version
invoke docs         # Build docs
invoke publish      # Publish to PyPI
```

## Test Configuration

- Tests require Django (configured in `tests/conftest.py`)
- Django requirement is version-gated: Django 1.11.29 for Python <3.9, Django 2.2.28 for >=3.9
- Coverage config in `.coveragerc` - branch coverage enabled, 80%+ target
- Tests use pytest with hypothesis for property-based testing
- Test files mirror module structure: `test_ttcal_day.py`, `test_ttcal_month.py`, `test_ttcal_year.py`, etc.

## CI/CD

GitHub Actions workflow (`.github/workflows/ci-cd.yml`):
- **Linting**: flake8 with max line length 199
- **Testing**: pytest across Python 3.8-3.11 on Ubuntu
- **Publishing**: Automatic PyPI deployment on version tags (`refs/tags/v*`)

## Important Quirks

1. **Norwegian Localization**: Day/month names are in Norwegian by default
   - `Day.day_name` = Norwegian weekday names
   - `Month.month_name` = Norwegian month names

2. **ISO Week Semantics**: Week numbering follows ISO 8601
   - Week 1 contains January 4th
   - Weeks can span calendar years
   - Thursday determines the ISO year of a week

3. **Member Month**: Days in calendar views track which month they're displayed in via `membermonth`, allowing weeks that span months to render correctly. When `Month` creates its weeks, all days in those weeks (including days from adjacent months) preserve their `membermonth` for consistent calendar grid rendering

4. **Django Integration**: The library includes Django template tags (`ttcal/templatetags/ttcal_tags.py`)

## Version Information

Current version: 2.0.5 (defined in both `setup.py` and `ttcal/__init__.py`)
