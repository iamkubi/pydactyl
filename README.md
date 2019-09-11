# pydactyl

[![Latest build][travis-img]][travis]
[![Latest docs][docs-img]][docs]
[![Coverage][codecov-img]][codecov]
[![Latest version][pypi-img]][pypi]

An easy to use Python wrapper for the Pterodactyl Panel API.

## State of the project

This wrapper is still very much a work in progress.  Not all APIs are 
implemented, and the way results are returned will definitely be changing in 
the near future.  Yes, that hideous way of getting the server identifier will
be changed to a server object with properties, because that srv_id example is 
terrible.

If you do encounter problems, find APIs that haven't been implemented, or 
have a feature request please file a [Github issue][issues].

## Installing

An early version of the package can be found on pip, however it won't be 
updated until the interface is more solidified.  A more feature complete 
version should be available soon.

To install the pip version:

```shell
pip install py_dactyl
```

New versions won't be published to pip every day, so until the rate of change
slows down the only way to get the latest version will be from Github.


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