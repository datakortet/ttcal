"core.fstr"

# pylint:disable=R0904
# R0904: Too many public methods
import pytest
from ttcal.day import fstr, fjoin

    
def test_split():
    "Test of the split method."
    r = fstr('D2008022002')
    
    assert r.split(1, 5, 7, 9) == ['D', '2008', '02', '20', '02']
    assert fstr('0123456789').split() == ['0123456789']
    assert fstr('0123456789').split(5) == ['01234', '56789']
    assert fstr('0123456789').split(3, 6) == ['012', '345', '6789']
    assert fstr('0123456789').split(2, 4, 6) == ['01', '23', '45', '6789']

    assert fstr('').split() == ['']
    assert fstr('').split(1) == ['']
    assert fstr('').split(1, 2) == ['']
    assert fstr('x').split(0) == ['x']
    assert fjoin(['x'], 0) == 'x'

    assert fstr('xx').split(0) == ['xx']
    assert fstr('xx').split(1) == ['x', 'x']

    fstr('hello').split(1, 2, 2) == ['h', 'el', 'lo']
    fstr('hello').split(1, 2) == ['h', 'el', 'lo']
