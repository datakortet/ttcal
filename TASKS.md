# 📝 Current Developer Tasks - ttcal

This file contains detailed implementation plans for the current active task(s).

**Status**: No active tasks yet - Ready to begin

## How to Use This File

1. Pick a task from TODO.md
2. Document the plan here with implementation details
3. Execute the task
4. Update SUMMARIES.md when complete
5. Mark task done in TODO.md and remove from here

## Active Task: Add Comprehensive Type Hints

**Priority**: 🟡 High

**Estimated Time**: 4-6 hours

**Started**: 2025-11-07

### Objective
Add comprehensive type hints across all modules to improve IDE support, documentation, and catch potential type errors early. Currently only `day.py` has minimal type hints.

### Files to Modify
- [ ] `ttcal/month.py` - All methods lack type hints (~30 methods)
- [ ] `ttcal/year.py` - All methods lack type hints (~40 methods)
- [ ] `ttcal/week.py` - All methods lack type hints (~20 methods)
- [ ] `ttcal/quarter.py` - All methods lack type hints (~20 methods)
- [ ] `ttcal/duration.py` - Complete partial coverage (~15 methods)
- [ ] `ttcal/calfns.py` - Add hints to helper functions (~5 functions)
- [ ] `ttcal/day.py` - Enhance existing minimal hints

### Implementation Plan
1. Start with `month.py` as it's a core class
2. Add imports: `from typing import Optional, List, Tuple, Union, Iterator, Any, ClassVar`
3. Add `from __future__ import annotations` for forward references
4. Type all public methods, properties, and class methods
5. Type private methods where it improves clarity
6. Use `datetime.date` and `datetime.datetime` types where applicable
7. Test after each file to ensure no regressions
8. Document any complex type annotations

### Type Hints Strategy
```python
# Import pattern for each file
from __future__ import annotations
from typing import Optional, List, Tuple, Union, Iterator, Any, ClassVar
import datetime

# Method signatures examples:
def __init__(self, year: Optional[int] = None, month: Optional[int] = None) -> None:
def from_idtag(cls, tag: str) -> Month:
def parse(cls, txt: Optional[str]) -> Optional[Month]:
@property
def first(self) -> Day:
def __add__(self, n: int) -> Month:
def __eq__(self, other: object) -> bool:
def format(self, fmt: Optional[str] = None) -> str:
```

### Testing Strategy
```bash
# After each file, run tests
workon ttcal311 && pytest tests/test_ttcal_month.py -v
workon ttcal311 && pytest tests/test_ttcal_year.py -v
workon ttcal311 && pytest tests/test_ttcal_week.py -v
workon ttcal311 && pytest tests/test_ttcal_quarter.py -v

# Run full suite when done
workon ttcal311 && pytest -vv tests/

# Optional: Install and run mypy
pip install mypy
mypy ttcal/ --ignore-missing-imports
```

### Success Criteria
- [x] All public methods have type hints
- [x] All properties have return type annotations
- [x] Class methods properly typed with cls parameter
- [x] Complex types documented in comments where needed
- [x] All tests passing without modification
- [ ] Optional: mypy runs without errors

### Notes
- Maintain backward compatibility - type hints are annotations only
- Some circular dependencies may require `from __future__ import annotations`
- Use `Optional[T]` for nullable parameters
- Use `Union[T1, T2]` for multiple acceptable types
- For Django compatibility, may need `Any` in some places

---

## Task Template

When starting a task, copy this template below and fill it in:

```markdown
## Task: [Task Name]

**Priority**: 🔴 Critical / 🟡 High / 🟠 Medium / 🟢 Low

**Estimated Time**: [X hours]

**Started**: [Date]

### Objective
[What are we trying to accomplish?]

### Files to Modify
- [ ] `path/to/file.py` - [what changes]
- [ ] `path/to/other.py` - [what changes]

### Implementation Plan
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Testing Strategy
```bash
# Commands to run
workon ttcal311 && pytest tests/test_specific.py -v
```

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] All tests passing
- [ ] No new linting errors

### Notes
[Any additional context, gotchas, or considerations]
```

---

## Testing Reference

### Run Tests
```bash
# Full test suite with coverage
workon ttcal311 && pytest -vv --cov=ttcal tests

# Specific test file
workon ttcal311 && pytest tests/test_ttcal_day.py -v

# Single test
workon ttcal311 && pytest tests/test_ttcal_day.py::test_function_name -v

# Watch mode (if supported)
workon ttcal311 && pytest-watch tests/
```

### Linting
```bash
# Flake8 (used in CI)
flake8 ttcal/** --max-line-length=199

# pep8 via dk
dk pep8

# pylint via dk
dk pylint
```

### Type Checking (after adding type hints)
```bash
# Install mypy if needed
pip install mypy

# Run type checker
mypy ttcal/ --ignore-missing-imports
```

### Build and Install Locally
```bash
# Build distribution
python setup.py sdist bdist_wheel

# Install in development mode
pip install -e .
```

## Important Implementation Notes

### Code Style Guidelines
- Use f-strings for string formatting (not % or .format())
- Follow existing patterns in the codebase
- Maintain backward compatibility
- Keep line length under 199 characters (flake8 setting)
- Use descriptive variable names
- Add docstrings for new functions/methods

### Type Hints Style (when adding)
```python
from typing import Optional, List, Tuple, Union
from datetime import date, datetime

def method_name(param: int, optional_param: Optional[str] = None) -> Tuple[int, str]:
    """Docstring here."""
    ...
```

### Testing Patterns
```python
# Test file structure
def test_feature_name():
    """Test description."""
    # Arrange
    obj = Day(2024, 1, 15)

    # Act
    result = obj.some_method()

    # Assert
    assert result == expected_value
```

### i18n Pattern (when implementing)
```python
# Proposed pattern for locale support
from ttcal.locale import get_locale, _

# In code:
locale = get_locale()  # Returns current locale
day_name = _(locale.day_names[index])
```

## Git Workflow

### Branch Naming
```bash
# Feature branches
git checkout -b feature/i18n-support
git checkout -b fix/remove-debug-print
git checkout -b refactor/type-hints

# Current branch
git checkout master  # Main development branch
```

### Commit Message Style
```
[type]: Short description (50 chars or less)

Longer explanation if needed (wrap at 72 characters)

- Bullet points for multiple changes
- Reference issue numbers if applicable

Fixes #123
```

Types: feat, fix, refactor, docs, test, chore

## Key Architectural Reminders

### Circular Dependencies
- Day.Month, Day.Year, Day.week are added as properties at end of respective modules
- Don't try to import at top of file - will cause circular import

### Comparison Operators
- All calendar classes use `rangetuple()` and `rangecmp()` from `calfns.py`
- Comparison is based on interval overlap (not point comparison)

### idtag System
- Each class has `.idtag()` instance method
- Each class has `.from_idtag(tag)` class method
- Top-level `from_idtag(tag)` auto-detects type from first character

### Period Arithmetic
- `Day + int` adds days (returns new Day)
- `Day + Period` adds months/years with smart month-end handling
- Period handles edge cases: Jan 31 + 1 month = Feb 28/29

## Reference Links

### Documentation
- README.rst: Project overview and usage examples
- CLAUDE.md: Comprehensive architecture and development guide
- TODO.md: All prioritized tasks and improvements

### CI/CD
- `.github/workflows/ci-cd.yml`: GitHub Actions configuration
- Tests run on: Python 3.8, 3.9, 3.10, 3.11
- Auto-deploy to PyPI on version tags

### Related Files
- `dkbuild.yml`: Build configuration for dk tool
- `tasks.py`: invoke task definitions
- `.coveragerc`: Coverage configuration
