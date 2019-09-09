# pydactyl

[![Latest build][travis-img]][travis]
[![Latest docs][docs-img]][docs]
[![Latest version][pypi-img]][pypi]
[![Coverage][codecov-img]][codecov]


An easy to use Python wrapper for the Pterodactyl Panel API.

## Getting Started

```python
from pydactyl import PterodactylClient

# Create a client to connect to the panel and authenticate with your API key.
client = PterodactylClient('https://panel.mydomain.com', 'MySuperSecretApiKey')

# Get a list of all servers the user has access to
my_servers = client.client.list_servers()
# Get the unique identifier for the first server.
srv_id = my_servers['data'][0]['attributes']['identifier']

# Check the utilization of the server
srv_utilization = client.client.get_server_utilization(srv_id)
print(srv_utilization)
```

[docs]: https://pydactyl.readthedocs.io/
[docs-img]: https://readthedocs.org/projects/pydactyl/badge/?version=latest (Latest docs)
[pulls]: https://github.com/iamkubi/pydactyl/pulls
[issues]: https://github.com/iamkubi/pydactyl/issues
[pypi]: https://pypi.python.org/pypi/py-dactyl/
[pypi-img]: https://img.shields.io/pypi/v/py-dactyl.svg
[travis]: https://travis-ci.org/iamkubi/pydactyl
[travis-img]: https://travis-ci.org/iamkubi/pydactyl.svg?branch=master
[codecov]: https://codecov.io/gh/iamkubi/pydactyl
[codecov-img]: https://codecov.io/gh/iamkubi/pydactyl/branch/master/graph/badge.svg