from pydactyl.api.base import PterodactylAPI
from pydactyl.constants import USE_SSL


class Nodes(PterodactylAPI):
    """Class for interacting with the Pterdactyl Nodes API."""

    def list_nodes(self):
        """List all nodes."""
        response = self._api_request(endpoint='application/nodes')
        return response

    def get_node_info(self, node_id):
        """Get detailed info for the specified node.

        Args:
            node_id(int): Pterodactyl Node ID.
        """
        response = self._api_request(endpoint='application/nodes/%s' % node_id)
        return response

    def create_node(self, name, description, location_id, fqdn, memory, disk, memory_overallocate=0,
                    disk_overallocate=0, use_ssl=True, behind_proxy=False, daemon_base='/srv/daemon-data',
                    daemon_sftp=2022, daemon_listen=8080, upload_size=100, public=True, maintenance_mode=False):
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

    def edit_node(self, node_id, shortcode=None, description=None):
        """Modify an existing node.

        Args:
            node_id(int): Pterodactyl Node ID.
            shortcode(str): Short identifier between 1 and 60 characters, e.g. us.nyc.lvl3
            description(str): A long description of the node.  Max 255 characters.
        """
        if not shortcode and not description:
            raise BadRequestError('Must specify either shortcode or description for edit_node.')

        data = {}
        if shortcode:
            data['shortcode'] = shortcode
        if description:
            data['description'] = description

        response = self._api_request(endpoint='application/nodes/%s' %
                                              node_id, mode='PATCH', data=data)
        return response

    def delete_node(self, node_id):
        """Delete an existing node.

        Args:
            node_id(int): Pterodactyl Node ID.
        """
        response = self._api_request(endpoint='application/nodes/%s' %
                                              node_id, mode='DELETE')
        return response
