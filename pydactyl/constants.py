"""Pydactyl constants."""

__version__ = '1.0.1'

USER_AGENT = 'Pydactyl/' + __version__
POWER_SIGNALS = ('start', 'stop', 'restart', 'kill')
USE_SSL = {True: 'https', False: 'http'}
REQUEST_TYPES = ('GET', 'POST', 'PATCH', 'DELETE', 'PUT')
