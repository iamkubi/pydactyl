# pydactyl

[![Latest build][travis-img]][travis]
[![Latest docs][docs-img]][docs]
[![Coverage][codecov-img]][codecov]
[![Latest version][pypi-img]][pypi]

An easy to use Python wrapper for the Pterodactyl Panel API.

## State of the project

This wrapper is mostly complete for Pterodactyl 0.7.  If you encounter problems, find APIs that haven't been implemented, or 
have a feature request please file a [Github issue][issues].

## Installing

An early version of the package can be found on pip, however it won't be 
updated until the interface is more solidified.  A more feature complete 
version should be available soon.

To install the pip version:

```shell
pip install py-dactyl
```

New versions won't be published to pip every day, so until the rate of change
slows down the only way to get the latest version will be from Github.


## Getting Started

Pterodactyl has two different types of API keys: Client (also known as Account) and Application.  Any user can generate an Account API key to control their own servers.  The Account API key for an Administrator user will be able to access any server's Client API.  The Client API does not contain any destructive functions, so it is relatively safe to experiment with.

Application API keys can only be generated my administrators.  These keys can be used to create, modify, and delete servers, among other things.  They have access to any server on the panel and can be destructive, so use with care.

### Client API
The Client API or Account API is accessed by users of the Pterodactyl panel.  Below are examples of how you might get information about y our servers.

```python
from pydactyl import PterodactylClient

# Create a client to connect to the panel and authenticate with your API key.
client = PterodactylClient('https://panel.mydomain.com', 'MySuperSecretApiKey')

# Get a list of all servers the user has access to
my_servers = client.client.list_servers()
# Get the unique identifier for the first server.
srv_id = my_servers[0]['identifier']

# Check the utilization of the server
srv_utilization = client.client.get_server_utilization(srv_id)
print(srv_utilization)

# Turn the server on.
client.client.send_power_action(srv_id, 'start')
```

### Application API
The Application API is the administrative API of the Ptoerdactyl panel.  Below are examples of how you might use this API.

```python
from pydactyl import PterdoactylClient

# Create a client to connect to the panel and authenticate with your API key.
client = PterodactylClient('https://panel.mydomain.com', 'MySuperSecretApiKey')

# Create a server.  Customize the Nest and Egg IDs to match the IDs in your panel.
# This server is created with a limit of 8000 MB of memory, no access to swap, unlimited disk space, in location_id 1.
client.servers.create_server(name='My Paper Server', user_id=1, nest_id=1, 
                             egg_id=3, memory_limit=8000, swap_limit=0, 
                             disk_limit=0, location_ids=[1])
<Response [201]>
```

A 201 response indicates success, however if there is a problem with the
 request Pydactyl will raise an exception with additional details.  When
  updating the location_ids field to an invalid location it displays an error: 
 
 ```python
client.servers.create_server(name='My Paper Server', user_id=1, nest_id=1, 
                             egg_id=3, memory_limit=8000, swap_limit=0, 
                             disk_limit=0, location_ids=[199])
Traceback (most recent call last):
  File "<input>", line 6, in <module>
  File "D:\code\pydactyl\pydactyl\api\servers.py", line 268, in create_server
    mode='POST', data=data, json=False)
  File "D:\code\pydactyl\pydactyl\api\base.py", line 98, in _api_request
    'code'], errors['detail'])
pydactyl.exceptions.PterodactylApiError: Bad API Request(400) - NoViableNodeException - No nodes satisfying the requirements specified for automatic deployment could be found.
```

You can use the User class to add, modify, and delete panel users.

```python
# Create a new user
result = client.user.create_user('test_user', 'test@gmail.com', 'Test', 'Name')
# Get the ID of the created user
user_id = result['attributes']['id']
# Get the user info, also returned by create_user()
client.user.get_user_info(user_id)
{'object': 'user', 'attributes': {'id': 14, 'external_id': None, ....
# Delete the user
client.user.delete_user(user_id=14)
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
