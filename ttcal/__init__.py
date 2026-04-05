"""
Date classes (originally from TikTok).
"""
__version__ = '2.0.9'
from .day import Day, Days, Today   # noqa  
from .duration import Duration, Period  # noqa
from .calfns import chop, isoweek   # noqa
from .month import Month
from .week import Week
from .year import Year
from .quarter import Quarter


def from_idtag(idtag):
    """Return a class from idtag.
    """
    if len(idtag) <= 1 or idtag[0] not in 'wdmqy':
        raise ValueError(f'Invalid idtag: {idtag!r}')

    return {
        'w': Week,
        'd': Day,
        'm': Month,
        'q': Quarter,
        'y': Year,
    }[idtag[0]].from_idtag(idtag)
