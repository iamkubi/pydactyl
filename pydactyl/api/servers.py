from pydactyl.api import base
from pydactyl.exceptions import BadRequestError


class Servers(base.PterodactylAPI):
    """Class for interacting with the Pterdactyl Servers API."""

    def list_servers(self, detail=False):
        """List all servers.

        Args:
            detail(bool): If True includes created and updated timestamps.
        """
        response = self._api_request(endpoint='application/servers')
        return base.parse_response(response, detail)

    def get_server_info(self, server_id=None, external_id=None, detail=False):
        """Get detailed info for the specified server.

        Args:
            server_id(int): Pterodactyl Server ID.
            external_id(int): Server ID from an external system like WHMCS
            detail(bool): If True includes created and updated timestamps.
        """
        if not server_id and not external_id:
            raise BadRequestError('Must specify either server_id or '
                                  'external_id.')
        if server_id and external_id:
            raise BadRequestError('Specify either server_id or external_id, '
                                  'not both.')

        if server_id:
            endpoint = 'application/servers/%s' % server_id
        else:
            endpoint = 'application/servers/external/%s' % external_id

        response = self._api_request(endpoint=endpoint)
        return base.parse_response(response, detail)

    def suspend_server(self, server_id):
        """Suspend the server with the specified internal ID.

        Args:
            server_id(int): Pterodactyl Server ID.
        """
        response = self._api_request(
            endpoint='application/servers/%s/suspend' % server_id, mode='POST')
        return response

    def unsuspend_server(self, server_id):
        """Suspend the server with the specified internal ID.

        Args:
            server_id(int): Pterodactyl Server ID.
        """
        response = self._api_request(
            endpoint='application/servers/%s/unsuspend' % server_id,
            mode='POST')
        return response

    def reinstall_server(self, server_id):
        """Reinstall the server with the specified internal ID.

        Args:
            server_id(int): Pterodactyl Server ID.
        """
        response = self._api_request(
            endpoint='application/servers/%s/reinstall' % server_id,
            mode='POST')
        return response

    def rebuild_server(self, server_id):
        """Rebuild the server with the specified internal ID.

        Args:
            server_id(int): Pterodactyl Server ID.
        """
        response = self._api_request(
            endpoint='application/servers/%s/rebuild' % server_id,
            mode='POST')
        return response

    def delete_server(self, server_id, force=False):
        """Delete the server with the specified internal ID.

        Attempts to delete the server from both the panel and daemon.
        By default if either one reports an error the action will be cancelled.

        Args:
            server_id(int): Pterodactyl Server ID.
            force(bool): If True the delete action will continue if the panel or
                    daemon reports an error.
        """
        endpoint = 'application/servers/%s' % server_id
        if force:
            endpoint += '/force'

        response = self._api_request(endpoint=endpoint, mode='DELETE')
        return response

    def list_server_databases(self, server_id, detail=False):
        """List the database servers assigned to the specified server ID.

        Args:
            server_id(int): Pterodactyl Server ID.
            detail(bool): If True includes the object type and a nested data
                    structure.
        """
        response = self._api_request(
            endpoint='application/servers/%s/databases' % server_id)
        return base.parse_response(response, detail)

    def get_server_database_info(self, server_id, database_id, detail=False):
        """Get information about the specified database on the specified server.

        Args:
            server_id(int): Pterodactyl Server ID.
            database_id(int): Database ID for specified server.
            detail(bool): If True includes the object type and a nested data
                    structure.
        """
        response = self._api_request(
            endpoint='application/servers/%s/databases/%s' % (server_id,
                                                              database_id))
        return base.parse_response(response, detail)

    def create_server_database(self, server_id):
        """Create a database for the specified server.

        Args:
            server_id(int): Pterodactyl Server ID.
        """
        response = self._api_request(
            endpoint='application/servers/%s/databases' % server_id,
            mode='POST')
        return response

    def delete_server_database(self, server_id, database_id):
        """Delete the specified database for the specified server.

        Args:
            server_id(int): Pterodactyl Server ID.
            database_id(int): Database ID for specified server.
        """
        response = self._api_request(
            endpoint='application/servers/%s/databases/%s' % (server_id,
                                                              database_id),
            mode='DELETE')
        return response

    def reset_server_database_password(self, server_id, database_id):
        """Resets the password for the specified server database.

        Args:
            server_id(int): Pterodactyl Server ID.
            database_id(int): Database ID for specified server.
        """
        response = self._api_request(
            endpoint='application/servers/%s/databases/%s/reset-password' % (
                server_id,
                database_id),
            mode='POST')
        return response

    def create_server(self, name, user_id, nest_id, egg_id, memory_limit,
                      swap_limit, disk_limit, location_ids, port_range=[],
                      environment={}, cpu_limit=0, io_limit=500,
                      database_limit=0, allocation_limit=0,
                      docker_image=None, startup_cmd=None, dedicated_ip=False,
                      start_on_completion=True, oom_disabled=True):
        """Creates one or more servers in the specified locations.

        Creates server instance(s) and begins the install process using the
        specified configurations and limits.  If more than one value is
        specified for location_ids then identical servers will be created in
        each location.

        Args:
            name(str): Name of the server to display in the panel.
            user_id(int): User ID that will own the server.
            nest_id(int): Nest ID for the created server.
            egg_id(int): Egg ID for the created server.
            memory_limit(int): Memory limit in MB for the Docker container.  To
                    allow unlimited memory limit set to 0.
            swap_limit(int): Swap limit in MB for the Docker container.  To not
                    assign any swap set to 0.  For unlimited swap set to -1.
            disk_limit(int): Disk limit in MB for the Docker container.  To
                    allow unlimited disk space set to 0.
            environment(dict): Key value pairs of Service Variables to set.
                    Every variable from the egg must be set or the API will
                    return an error.  Default values will be pulled from the egg
                    config or set to None.
            location_ids(iter): List of location_ids where the server(s) will be
                    created.  If more than one location is specified
                    identical servers will be created at each.
            port_range(iter): List of ports or port ranges to use when
                    selecting an allocation.  If empty, all ports will be
                    considered.  If set, only ports appearing in the list or
                    range will be used.  e.g. [20715, '20815-20915']
            cpu_limit(int): CPU limit for the Docker container.  To allow
                    unlimited CPU usage set to 0.  To limit to one core set
                    to 100.  For four cores set to 400.
            io_limit(int): Block IO weight for the Docker container.
                    Must be between 10 and 1000.
            database_limit(int): Maximum number of databases that can be
                    assigned to this server.
            allocation_limit(int): Maximum number of allocations that can be
                    assigned to this server.
            docker_image(str): Name or URL of the Docker server to use.
                    e.g. quay.io/pterodactyl/core:java-glibc
            startup_cmd(str): Startup command, if specified replaces the
                    egg's default value.
            dedicated_ip(bool): Limit allocations to IPs without any existing
                    allocations.
            start_on_completion(bool): Start server after install completes.
            oom_disabled(bool): Disables OOM-killer on the Docker container.
        """
        # Fetch the Egg variables which are required to create the server.
        egg_info = self._api_request(
            endpoint='application/nests/%s/eggs/%s' % (
                nest_id, egg_id), params={'include': 'variables'})['attributes']
        egg_vars = egg_info['relationships']['variables']['data']

        # Build a dict of environment variables.  Prefer values passed in the
        # environment parameter, otherwise use the default value from the Egg
        # config.
        env_with_defaults = {}
        for var in egg_vars:
            var_name = var['attributes']['env_variable']
            if var_name in environment:
                env_with_defaults = environment[var_name]
            else:
                env_with_defaults[var_name] = var['attributes'].get(
                    'default_value')

        if not docker_image:
            docker_image = egg_info.get('docker_image')
        if not startup_cmd:
            startup_cmd = egg_info.get('startup')

        data = {
            'name': name,
            'user': user_id,
            'nest': nest_id,
            'egg': egg_id,
            'docker_image': docker_image,
            'startup': startup_cmd,
            'oom_disabled': oom_disabled,
            'limits': {
                'memory': memory_limit,
                'swap': swap_limit,
                'disk': disk_limit,
                'io': io_limit,
                'cpu': cpu_limit,
            },
            'feature_limits': {
                'databases': database_limit,
                'allocations': allocation_limit,
            },
            'environment': env_with_defaults,
            'deploy': {
                'locations': location_ids,
                'dedicated_ip': dedicated_ip,
                'port_range': port_range,
            },
            'start_on_completion': start_on_completion,
        }

        response = self._api_request(endpoint='application/servers',
                                     mode='POST', data=data, json=False)
        return response
