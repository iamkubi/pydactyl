# pydactyl
======================

[![Latest docs][docs-img]][docs]


An easy to use Python wrapper for the Pterodactyl Panel API.

## Getting Started

```python
from pydactyl import PterodactylClient

# Create a client to connect to the panel and authenticate with your API key.
client = PterodactylClient('https://panel.mydomain.com', 'MySuperSecretApiKey')

# Get a list of all servers the user has access to
my_servers = client.client.list_servers()
# Get the unique identifier for the first server
srv_id = my_servers.json()['data'][0]['attributes']['identifier']

# Check the utilization of the server
srv_utilization = client.client.get_server_utilization(srv_id)
srv_utilization.json()
```