# TODO: ttcal - Calendar Operations Library

This file (TODO.md) is a high-level overview of the current priorities and improvements needed in the ttcal library.

The TASKS.md file is a detailed breakdown of the current task(s) being worked on.

The SUMMARIES.md file is a summary of past sessions and tasks completed.

Pick a task from the TODO.md file, write a plan for the task in the TASKS.md file, and write a summary of the session in the SUMMARIES.md file when you complete the task. When you complete the task, update the TODO.md file to reflect the task as completed and remove it from the TASKS.md file.

## 🔴 Critical Issues (Blocking)

### 1. ~~Remove Debug Print Statement~~ ✅ COMPLETED (2025-11-07)
- [x] **File**: `ttcal/templatetags/ttcal_tags.py:47`
- [x] **Issue**: Production debug print statement in `is_current()` function
- [x] **Impact**: Unwanted console output in production Django templates
- [x] **Fix**: Removed the print statement

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

### 2. ~~Add Comprehensive Type Hints~~ ✅ COMPLETED (2025-11-07)
- [x] **Issue**: Only minimal type hints in `day.py`, rest of codebase lacks annotations
- [x] **Impact**: Poor IDE support, unclear API contracts
- [x] **Files Needing Type Hints**:
  - `ttcal/month.py` - ✅ All methods now have type hints
  - `ttcal/year.py` - ✅ All methods now have type hints
  - `ttcal/week.py` - ✅ All methods now have type hints
  - `ttcal/quarter.py` - ✅ All methods now have type hints
  - `ttcal/calfns.py` - ✅ All functions now have type hints
  - `ttcal/duration.py` - ⚠️ Partial (left for separate task due to complexity)
- [x] **Solution**: Added type hints using Python 3.8+ syntax with `from __future__ import annotations`
- [x] **Testing**: All 159 tests passing without modification

## 🟠 Medium Priority (Code Quality)

### 3. ~~Modernize String Formatting~~ ✅ COMPLETED (2025-11-07)
- [x] **Issue**: Old-style `%` formatting used in several places
- [x] **Impact**: Inconsistent code style, less readable
- [x] **Files Updated**:
  - `ttcal/day.py:232` - Converted `__repr__` to f-string
  - `ttcal/day.py:367` - Converted `idtag` property to f-string
  - `ttcal/duration.py:147` - Converted `__repr__` to f-string
  - `ttcal/duration.py:189` - Converted `__str__` to f-string
- [x] **Solution**: Converted all to f-strings for consistency

### 4. ~~Remove Python 2 Compatibility Code~~ ✅ COMPLETED (2025-11-07)
- [x] **Issue**: Unnecessary Python 2 division compatibility code
- [x] **File**: `ttcal/duration.py:274-290`
- [x] **Fix**: Removed `__div__()` method, kept only `__truediv__()`
- [x] **Reasoning**: Project supports Python 3.8+ only

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

### 7. ~~File Operations Best Practices~~ ✅ COMPLETED (2025-11-07)
- [x] **Issue**: File reading without encoding specification
- [x] **File**: `setup.py:22`
- [x] **Fix**: Added `encoding='utf-8'` parameter to `open()`

### 8. Replace Assert with ValueError
- [ ] **Issue**: Bare `assert` used in public API
- [ ] **File**: `ttcal/month.py:74`
- [ ] **Current**: `assert None not in (year, month)`
- [ ] **Better**: Explicit `if` check with descriptive `ValueError`
- [ ] **Benefit**: Better error messages for users

### 9. ~~Remove setup.cfg Universal Wheel~~ ✅ COMPLETED (2025-11-07)
- [x] **Issue**: `universal = 1` flag suggests Python 2/3 compatibility
- [x] **File**: `setup.cfg:2`
- [x] **Fix**: Removed `[wheel]` section (Python 3 only)

### 10. ~~Add More Comprehensive Docstrings~~ ✅ COMPLETED (2025-11-07 Session 5)
- [x] **Issue**: Current docstrings are minimal
- [x] **Impact**: Poor API documentation
- [x] **Solution**: Added comprehensive docstrings with:
  - Parameter descriptions
  - Return type descriptions
  - Usage examples
  - Fixed typos in existing docstrings
- [x] **Files Updated**: All 7 Python modules
  - day.py - ~30 methods/properties enhanced
  - month.py - ~25 methods enhanced
  - year.py - ~20 methods enhanced
  - week.py - ~15 methods enhanced
  - quarter.py - ~20 methods enhanced
  - duration.py - ~20 methods enhanced
  - calfns.py - 4 functions enhanced
- [x] **All 159 tests passing**

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

### 2025-11-07

#### Session Part 4: String Formatting Modernization
- **Convert % Formatting to F-Strings** (Medium Priority)
  - Converted 4 occurrences in `day.py` and `duration.py`
  - Improved code readability and consistency
  - All 159 tests passing

#### Session Part 3: Quick Win Improvements
- **Remove Debug Print Statement** (Critical Priority)
  - Removed production debug print from `ttcal_tags.py:47`
- **File Encoding Specification** (Low Priority)
  - Added `encoding='utf-8'` to file open in `setup.py:22`
- **Remove Python 2 Compatibility** (Medium Priority)
  - Removed `__div__()` method from `duration.py`
- **Clean Setup Configuration** (Low Priority)
  - Removed universal wheel flag from `setup.cfg`
- All 159 tests passing after changes

#### Session Part 2: Type Hints Implementation
- **Add Comprehensive Type Hints** (High Priority)
  - Added type hints to 6 core modules (month.py, year.py, week.py, quarter.py, calfns.py)
  - ~110 methods/functions typed
  - All 159 tests passing
  - Used Python 3.8+ syntax with `from __future__ import annotations`
  - Improved IDE support and API documentation

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
