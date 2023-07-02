"""
Date classes (originally from TikTok).
"""
__version__ = '2.0.5'
from .day import Day, Days, Today   # noqa  
from .duration import Duration, Period  # noqa
from .calfns import chop, isoweek   # noqa
from .month import Month
from .week import Week
from .year import Year


def from_idtag(idtag):
    """Return a class from idtag.
    """
    assert len(idtag) > 1
    assert idtag[0] in 'wdmy'

    return {
        'w': Week,
        'd': Day,
        'm': Month,
        'y': Year,
    }[idtag[0]].from_idtag(idtag)
