# pydactyl

![lint-and-test]
[![Latest docs][docs-img]][docs]
[![Coverage][codecov-img]][codecov]
[![Latest version][pypi-img]][pypi]
[![Discord][discord-img]][discord-join]

An easy to use Python wrapper for the Pterodactyl Panel API.

## State of the project

Support for Pterodactyl 1.x endpoints is mostly completed, however some 
endpoints are still missing. Future versions will not attempt to remain
backwards compatible with versions of Pterodactyl before 1.0, however old
versions of pydactyl that do support 0.7 will remain available.

The 1.0 release is mostly stable and will not see significant changes until the
Pterodactyl 2.0 release. Pull Requests will still be accepted and new endpoints
will continue to be added. Pterodactyl API changes are expected in the 2.0
release, and there will likely be a refactor of the pydactyl interface at that
time. pydactyl 2.0 will be released once this work is completed.

If you encounter problems, find APIs that haven't been implemented, or have a
feature request please file a [Github issue][issues].

## Documentation

Generated documentation can be found at [https://pydactyl.readthedocs.io/][docs]
.

## Installing

To install with pip:

```shell
pip install py-dactyl
```

## Getting Started

Pterodactyl has two different types of API keys: Client (also known as Account) and Application.  Any user can generate an Account API key to control their own servers.  The Account API key for an Administrator user will be able to access any server's Client API.  The Client API does not contain any destructive functions, so it is relatively safe to experiment with.

Application API keys can only be generated by administrators.  These keys can be used to create, modify, and delete servers, among other things.  They have access to any server on the panel and can be destructive, so use with care.

### Client API
The Client API or Account API is accessed by users of the Pterodactyl panel.  Below are examples of how you might get information about your servers.

```python
from pydactyl import PterodactylClient

# Create a client to connect to the panel and authenticate with your API key.
api = PterodactylClient('https://panel.mydomain.com', 'MySuperSecretApiKey')

# Get a list of all servers the user has access to
my_servers = api.client.list_servers()
# Get the unique identifier for the first server.
srv_id = my_servers[0]['attributes']['identifier']

# Check the utilization of the server
srv_utilization = api.client.get_server_utilization(srv_id)
print(srv_utilization)

# Turn the server on.
api.client.send_power_action(srv_id, 'start')
```

### Application API
The Application API is the administrative API of the Pterodactyl panel.
Below are examples of how you might use this API.

```python
from pydactyl import PterodactylClient

# Create a client to connect to the panel and authenticate with your API key.
api = PterodactylClient('https://panel.mydomain.com', 'MySuperSecretApiKey')

# Create a server.  Customize the Nest and Egg IDs to match the IDs in your panel.
# This server is created with a limit of 8000 MB of memory, no access to swap, unlimited disk space, in location_id 1.
api.servers.create_server(name='My Paper Server', user_id=1, nest_id=1,
                          egg_id=3, memory_limit=8000, swap_limit=0,
                          backup_limit=0, disk_limit=0, location_ids=[1])
< Response[201] >
```

A 201 response indicates success, however if there is a problem with the request
Pydactyl will raise an exception with additional details. When updating the
location_ids field to an invalid location it displays an error:

 ```python
api.servers.create_server(name='My Paper Server', user_id=1, nest_id=1,
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
result = api.user.create_user('test_user', 'test@gmail.com', 'Test', 'Name')
# Get the ID of the created user
user_id = result['attributes']['id']
# Get the user info, also returned by create_user()
api.user.get_user_info(user_id)
{'object': 'user', 'attributes': {'id': 14, 'external_id': None, ....
# Delete the user
api.user.delete_user(user_id=14)
```

### Paginated Responses

Pydactyl API responses return a PaginatedResponse object that can be iterated
over to automatically fetch additional pages as required. It is currently only
used by get_node_allocations(), however in time all Pydactyl methods will return
this response.

```python
# Create a list of all ports
allocs = api.nodes.list_node_allocations(node_id)
ports = []
for page in allocs:
    for item in page.data:
        ports.append(item['attributes']['port'])
len(ports)
151
```

[docs]: https://pydactyl.readthedocs.io/
[docs-img]: https://readthedocs.org/projects/pydactyl/badge/?version=latest (Latest docs)
[pulls]: https://github.com/iamkubi/pydactyl/pulls
[issues]: https://github.com/iamkubi/pydactyl/issues
[pypi]: https://pypi.python.org/pypi/py-dactyl/
[pypi-img]: https://img.shields.io/pypi/v/py-dactyl.svg
[codecov]: https://codecov.io/gh/iamkubi/pydactyl
[codecov-img]: https://codecov.io/gh/iamkubi/pydactyl/branch/master/graph/badge.svg
[discord-img]: https://img.shields.io/badge/discord-join-7289DA.svg?logo=discord&longCache=true&style=flat

[discord-join]: https://discord.gg/TgZDHPB

[lint-and-test]: https://github.com/iamkubi/pydactyl/actions/workflows/lint-and-test.yml/badge.svg?branch=master (https://github.com/iamkubi/pydactyl/actions/workflows/lint-and-test.yml)