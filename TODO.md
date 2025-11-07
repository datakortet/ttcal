# TODO: ttcal - Calendar Operations Library

This file (TODO.md) is a high-level overview of the current priorities and improvements needed in the ttcal library.

The TASKS.md file is a detailed breakdown of the current task(s) being worked on.

The SUMMARIES.md file is a summary of past sessions and tasks completed.

Pick a task from the TODO.md file, write a plan for the task in the TASKS.md file, and write a summary of the session in the SUMMARIES.md file when you complete the task. When you complete the task, update the TODO.md file to reflect the task as completed and remove it from the TASKS.md file.

## 🔴 Critical Issues (Blocking)

### 1. Remove Debug Print Statement
- [ ] **File**: `ttcal/templatetags/ttcal_tags.py:47`
- [ ] **Issue**: Production debug print statement in `is_current()` function
- [ ] **Impact**: Unwanted console output in production Django templates
- [ ] **Fix**: Remove the print statement immediately

## 🟡 High Priority (Quality & Internationalization)

### 1. Internationalization (i18n) System
- [ ] **Issue**: Hardcoded Norwegian strings throughout codebase without i18n support
- [ ] **Impact**: Non-Norwegian users cannot use the library in their language
- [ ] **Files Affected**:
  - `ttcal/month.py:16-19` - Month names in Norwegian
  - `ttcal/day.py:78-79` - Day names in Norwegian
  - `ttcal/month.py:58` - Error message in Norwegian
  - `ttcal/week.py:103` - Week display string in Norwegian
- [ ] **Solution**:
  - Create `ttcal/locale.py` module with i18n support
  - Use `gettext` or custom translation system
  - Provide English and Norwegian translations
  - Make locale configurable (default: English)
  - Maintain backward compatibility

### 2. Add Comprehensive Type Hints
- [ ] **Issue**: Only minimal type hints in `day.py`, rest of codebase lacks annotations
- [ ] **Impact**: Poor IDE support, unclear API contracts
- [ ] **Files Needing Type Hints**:
  - `ttcal/month.py` - All methods lack type hints
  - `ttcal/year.py` - All methods lack type hints
  - `ttcal/week.py` - All methods lack type hints
  - `ttcal/quarter.py` - All methods lack type hints
  - `ttcal/duration.py` - Partial coverage, needs completion
- [ ] **Solution**: Add type hints using Python 3.8+ syntax
- [ ] **Testing**: Verify with `mypy --strict`

## 🟠 Medium Priority (Code Quality)

### 3. Modernize String Formatting
- [ ] **Issue**: Old-style `%` formatting used in several places
- [ ] **Impact**: Inconsistent code style, less readable
- [ ] **Files to Update**:
  - `ttcal/day.py:232` - `'%d-%d-%d-%d' % (...)`
  - `ttcal/day.py:368` - `'d%d%02d%02d%02d' % (...)`
  - `ttcal/duration.py:147` - `'%sDuration(...)' % dt`
  - `ttcal/duration.py:188` - `'%s%d:%02d:%02d' % (...)`
- [ ] **Solution**: Convert all to f-strings for consistency

### 4. Remove Python 2 Compatibility Code
- [ ] **Issue**: Unnecessary Python 2 division compatibility code
- [ ] **File**: `ttcal/duration.py:274-290`
- [ ] **Fix**: Remove `__div__()` method, keep only `__truediv__()`
- [ ] **Reasoning**: Project supports Python 3.8+ only

### 5. Clean Up Commented Code
- [ ] **Issue**: Large blocks of commented code creating maintenance burden
- [ ] **Files with Commented Code**:
  - `ttcal/week.py:171-230` - Entire `Weeks` class commented out
  - `ttcal/quarter.py:39-80` - Comparison operators commented out
  - `ttcal/day.py:544-550` - Commented `timetuple()` method
  - `ttcal/month.py:111-115, 126-131, 204-215` - Various commented methods
  - `ttcal/year.py:98-104, 309-312` - Commented methods
  - `ttcal/duration.py:292-305` - Commented reverse operations
- [ ] **Action**: Either restore functionality or remove entirely
- [ ] **Document**: If keeping for reference, add explanation in comments

### 6. Fix Quarter Comparison Operators
- [ ] **Issue**: Quarter class has `__lt__`, `__le__`, `__gt__`, `__ge__` commented out
- [ ] **Impact**: API inconsistency with Day/Month/Week/Year classes
- [ ] **File**: `ttcal/quarter.py:39-80`
- [ ] **Options**:
  - Uncomment and test operators
  - Remove if intentionally unsupported
  - Document why if there's a design reason

## 🟢 Low Priority (Nice to Have)

### 7. File Operations Best Practices
- [ ] **Issue**: File reading without encoding specification
- [ ] **File**: `setup.py:22`
- [ ] **Fix**: Add `encoding='utf-8'` parameter to `open()`

### 8. Replace Assert with ValueError
- [ ] **Issue**: Bare `assert` used in public API
- [ ] **File**: `ttcal/month.py:74`
- [ ] **Current**: `assert None not in (year, month)`
- [ ] **Better**: Explicit `if` check with descriptive `ValueError`
- [ ] **Benefit**: Better error messages for users

### 9. Remove setup.cfg Universal Wheel
- [ ] **Issue**: `universal = 1` flag suggests Python 2/3 compatibility
- [ ] **File**: `setup.cfg:2`
- [ ] **Fix**: Remove `[wheel]` section (Python 3 only)

### 10. Add More Comprehensive Docstrings
- [ ] **Issue**: Current docstrings are minimal
- [ ] **Impact**: Poor API documentation
- [ ] **Solution**: Add comprehensive docstrings with:
  - Parameter descriptions
  - Return type descriptions
  - Usage examples
  - Edge case notes

### 11. Extract Comparison Logic to Mixin
- [ ] **Issue**: Comparison operators duplicated across 5 classes
- [ ] **Files**: Day, Month, Week, Year, Quarter
- [ ] **Pattern**: All use `rangetuple()`/`rangecmp()` pattern
- [ ] **Solution**: Create `RangeComparableMixin` to reduce duplication

## ⚪ Future Enhancements

### 12. Refactor Large Classes
- [ ] **Issue**: Classes flagged with `# pylint:disable=too-many-public-methods`
- [ ] **Files**: `day.py` (550 lines), `month.py` (379 lines), `year.py` (375 lines)
- [ ] **Consider**: Breaking into focused classes or using composition

### 13. Improved Test Coverage
- [ ] **Current**: Good coverage with pytest + hypothesis
- [ ] **Enhancement**: Add coverage reporting in CI/CD
- [ ] **Target**: 95%+ coverage on critical paths

### 14. Performance Profiling
- [ ] **Task**: Profile common operations
- [ ] **Optimize**: Frequently used methods (arithmetic, parsing, formatting)

## ✅ Completed Tasks

_(No completed tasks yet - this is a new improvement initiative)_

## Quick Reference

### Testing Commands
```bash
# Run all tests with coverage (using venv ttcal311)
workon ttcal311 && pytest -vv --cov=ttcal tests

# Run specific test file
workon ttcal311 && pytest tests/test_ttcal_day.py -v

# Run single test
workon ttcal311 && pytest tests/test_ttcal_day.py::test_function_name -v

# Linting
flake8 ttcal/** --max-line-length=199
dk pep8
dk pylint
```

### Project Structure
```
ttcal/
├── ttcal/              # Main package
│   ├── day.py         # Day, Days, Today classes
│   ├── month.py       # Month class
│   ├── year.py        # Year class
│   ├── week.py        # Week class
│   ├── quarter.py     # Quarter class
│   ├── duration.py    # Duration and Period classes
│   ├── calfns.py      # Helper functions
│   └── templatetags/  # Django template integration
├── tests/             # Test suite
└── docs/              # Documentation
```

### Key Architectural Patterns
- **Polymorphic Range API**: All calendar objects support `.first`, `.last`, `.rangetuple()`, `.between_tuple()`
- **idtag Serialization**: Each class has `.idtag()` method and `.from_idtag()` class method
- **Late Property Binding**: Circular dependencies resolved by adding properties at module end
- **Period vs Duration**: Period is semantic (months/years), Duration is fixed (timedelta)

### Python Version Support
- Minimum: Python 3.8
- Tested: Python 3.8, 3.9, 3.10, 3.11
- CI/CD: GitHub Actions with matrix testing
