# 📝 Current Developer Tasks - ttcal

This file contains detailed implementation plans for the current active task(s).

**Status**: No active tasks yet - Ready to begin

## How to Use This File

1. Pick a task from TODO.md
2. Document the plan here with implementation details
3. Execute the task
4. Update SUMMARIES.md when complete
5. Mark task done in TODO.md and remove from here

## No Active Task

**Status**: ✅ Previous task completed successfully (Quick Win Improvements)

## Available Tasks (from TODO.md)

### High Priority:
1. Implement i18n system (multiple files, days)

### Medium Priority:
1. Convert % formatting to f-strings (multiple files, hours)
2. Clean up commented code blocks (multiple files, hours)
3. Fix Quarter comparison operators (`quarter.py:39-80`)

### Low Priority:
1. Replace assert with ValueError (`month.py:74`)
2. Add comprehensive docstrings
3. Extract comparison logic to mixin
4. Refactor large classes

## Completed Today
✅ Type Hints Implementation (Part 2)
✅ Quick Win Improvements (Part 3)

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
