from pydactyl.api.base import PterodactylAPI
from pydactyl.constants import USE_SSL
from pydactyl.responses import PaginatedResponse


class Nodes(PterodactylAPI):
    """Class for interacting with the Pterdactyl Nodes API."""

    def list_nodes(self, includes=None, params=None):
        """List all nodes.

        Args:
            includes(iter): List of includes, e.g. ('allocations', 'servers')
            params(dict): Extra parameters to pass, e.g. {'per_page': 300}
        """
        endpoint = 'application/nodes'
        response = self._api_request(endpoint=endpoint,
                                     includes=includes, params=params)
        return PaginatedResponse(self, endpoint, response)

    def get_node_config(self, node_id):
        """Get the Wings configuration for the specified node.

        Args:
            node_id(int): Pterodactyl Node ID.
        """
        response = self._api_request(
            endpoint='application/nodes/{}/configuration'.format(node_id))
        return response

    def get_node_details(self, node_id, includes=None, params=None):
        """Get detailed info for the specified node.

        Args:
            node_id(int): Pterodactyl Node ID.
            includes(iter): List of includes, e.g. ('allocations', 'servers')
            params(dict): Extra parameters to pass, e.g. {'per_page': 300}
        """
        response = self._api_request(
            endpoint='application/nodes/{}'.format(node_id),
            includes=includes, params=params)
        return response

    def get_node_info(self, node_id):
        """DEPRECATED: Use get_node_details"""
        print('DEPRECATED: Use get_node_details() instead of get_node_info()!')
        return self.get_node_details(node_id)

    def create_node(self, name, description, location_id, fqdn, memory, disk,
                    memory_overallocate=0,
                    disk_overallocate=0, use_ssl=True, behind_proxy=False,
                    daemon_base='/srv/daemon-data',
                    daemon_sftp=2022, daemon_listen=8080, upload_size=100,
                    public=True, maintenance_mode=False):
        """Creates a new node.

        Args:
            name(str): Node Name, 1-100 characters, valid characters: a-zA-Z0-9_.-[Space]
            description(str): A long description of the node.
            location_id(int): A valid Location ID
            fqdn(str): Domain name used to connect to the daemon.  Alternatively an IP address if not using SSL.
            memory(int): Memory in MB that is available to the daemon for allocation to servers.
            memory_overallocate(int): Percentage of memory that can be overallocated, e.g. 150
            disk(int): Disk space in MB that is available to the daemon for allocation to servers.
            disk_overallocate(int): Percentage of disk space that can be overallocated, e.g. 150
            use_ssl(bool): True to enable SSL, false for insecure HTTP
            behind_proxy(bool): Set to True if running behind a proxy like CloudFlare.  Skips certificate check on boot.
            daemon_base(str): Directory where server files will be stored.
            daemon_sftp(int): Port used by daemon for SFTP.
            daemon_listen(int): Port used by the daemon.
            public(bool): Set to False to prevent servers from being created on this node.
            maintenance_mode(bool): Set to True to disable the node or something.
        """
        data = locals()
        del data['self']
        del data['use_ssl']
        data['scheme'] = USE_SSL[use_ssl]

        response = self._api_request(endpoint='application/nodes',
                                     mode='POST', data=data)
        return response

    def edit_node(self, node_id, name=None, description=None,
                  location_id=None, fqdn=None, use_ssl=None,
                  behind_proxy=None, maintenance_mode=None, memory=None,
                  memory_overallocate=None, disk=None,
                  disk_overallocate=None, upload_size=None, daemon_sftp=None,
                  daemon_listen=None):
        """Update the configuration for an existing node.

        Modifies an existing node identified by node_id and updates any
        parameters that are passed.

        *** WARNING ***
        This endpoint currently requires that you specify all parameters in
        order to edit a node.  This will be updated in the future to
        automatically fetch existing values, however since multiple endpoints
        require this functionality it will be added in a common location.

        Args:
            node_id(int): Pterodactyl Node ID.

            name(str): Node name
            description(str): A long description of the node.  Max 255 characters.
            location_id(int): Location ID
            fqdn(str): Fully qualified domain name of the node
            use_ssl(bool): True to enable SSL, false for insecure HTTP
            behind_proxy(bool): Sets the node's behind_proxy
            maintenance_mode(bool): Set the node's maintenance_mode
            memory(int): Total memory available for the node in MB
            memory_overallocate(int): A percentage to overallocate, e.g. 20 for 120%
            disk(int): Total disk available for the node in MB
            disk_overallocate(int): A percentage to overallocate, e.g. 20 for 120%
            upload_size(int): Maximum size of uploads in file manager in MB
            daemon_sftp(int): Node's SFTP port (default 2022)
            daemon_listen(int): Wings listen port (default 8080)
        """
        data = locals()
        del data['self']
        del data['node_id']
        del data['use_ssl']
        data['scheme'] = USE_SSL[use_ssl]

        response = self._api_request(
            endpoint='application/nodes/{}'.format(node_id), mode='PATCH',
            data=data)
        return response

    def delete_node(self, node_id):
        """Delete an existing node.

        Args:
            node_id(int): Pterodactyl Node ID.
        """
        response = self._api_request(
            endpoint='application/nodes/{}'.format(node_id), mode='DELETE')
        return response

    def list_node_allocations(self, node_id, includes=None, params=None):
        """Retrieves all allocations for a specified node.

        Args:
            node_id(int): Pterodactyl Node ID.
            includes(iter): List of includes, e.g. ('node', 'server')
            params(dict): Extra parameters to pass, e.g. {'per_page': 300}

        Returns:
            obj: Iterable response that fetches pages as required.
        """
        endpoint = 'application/nodes/{}/allocations'.format(node_id)
        response = self._api_request(endpoint=endpoint, includes=includes,
                                     params=params)
        return PaginatedResponse(self, endpoint, response)

    def create_allocations(self, node_id, ip, ports, alias=None):
        """Create one or more allocations.

        Args:
            node_id(int): Pterodactyl Node ID.
            ip(str): The IP address to create the allocation on.
            ports(iter): List of strings representing strings.  Can use
                ranges as supported by Pterodactyl, e.g. ["4000", "4003-4005"]
            alias(str): Optional IP alias.  Used if you want to display a
                different IP address to Panel users, for example to display the
                external IP when behind a NAT.
        """
        data = {'ip': ip, 'ports': ports}
        if alias:
            data['alias'] = alias
        response = self._api_request(
            endpoint='application/nodes/{}/allocations'.format(node_id),
            mode='POST', data=data, json=False)
        return response

    def delete_allocation(self, node_id, allocation_id):
        """Deletes the specified allocation on the specified node.

        The Pterodactyl API currently limits delete_allocation to a single
        allocation per API call.

        See: https://github.com/pterodactyl/panel/issues/4373

        Args:
            node_id(int): Pterodactyl Node ID.
            allocation_id(int): Pterodactyl Allocation ID.  This is the
                internal ID assigned to the allocation, not the port number.
        """
        endpoint = 'application/nodes/{}/allocations/{}'.format(node_id,
                                                                allocation_id)
        response = self._api_request(
            endpoint=endpoint, mode='DELETE', json=False)
        return response

