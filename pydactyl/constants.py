"""Pydactyl constants."""

__version__ = '1.1.6'
USER_AGENT = 'Pydactyl/' + __version__

POWER_SIGNALS = ('start', 'stop', 'restart', 'kill')
REQUEST_TYPES = ('GET', 'POST', 'PATCH', 'DELETE', 'PUT')
SCHEDULE_ACTIONS = ('command', 'power', 'backup')
USE_SSL = {True: 'https', False: 'http'}
