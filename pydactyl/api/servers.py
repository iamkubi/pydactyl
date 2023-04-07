from pydactyl.api import base
from pydactyl.exceptions import BadRequestError
from pydactyl.responses import PaginatedResponse


class Servers(base.PterodactylAPI):
    """Class for interacting with the Pterdactyl Servers API."""

    def list_servers(self, includes=None, params=None):
        """List all servers.

        Args:
            includes(iter): List of includes, e.g. ('allocations', 'node')
            params(dict): Extra parameters to pass, e.g. {'per_page': 300}
        """
        endpoint = 'application/servers'
        response = base.parse_response(
            self._api_request(endpoint=endpoint, includes=includes,
                              params=params),
            detail=True)
        return PaginatedResponse(self, endpoint, response)

    def get_server_info(self, server_id=None, external_id=None, detail=False,
                        includes=None, params=None):
        """Get detailed info for the specified server.

        Args:
            server_id(int): Pterodactyl Server ID.
            external_id(int): Server ID from an external system like WHMCS
            detail(bool): If True includes created and updated timestamps.
            includes(iter): List of includes, e.g. ('egg', 'allocations')
            params(dict): Extra parameters to pass, e.g. {'per_page': 300}
        """
        if not server_id and not external_id:
            raise BadRequestError('Must specify either server_id or '
                                  'external_id.')
        if server_id and external_id:
            raise BadRequestError('Specify either server_id or external_id, '
                                  'not both.')

        if server_id:
            endpoint = 'application/servers/{}'.format(server_id)
        else:
            endpoint = 'application/servers/external/{}'.format(external_id)

        response = self._api_request(endpoint=endpoint, includes=includes,
                                     params=params)
        return base.parse_response(response, detail)

    def suspend_server(self, server_id):
        """Suspend the server with the specified internal ID.

        Args:
            server_id(int): Pterodactyl Server ID.
        """
        response = self._api_request(
            endpoint='application/servers/{}/suspend'.format(server_id),
            mode='POST')
        return response

    def unsuspend_server(self, server_id):
        """Suspend the server with the specified internal ID.

        Args:
            server_id(int): Pterodactyl Server ID.
        """
        response = self._api_request(
            endpoint='application/servers/{}/unsuspend'.format(server_id),
            mode='POST')
        return response

    def reinstall_server(self, server_id):
        """Reinstall the server with the specified internal ID.

        Args:
            server_id(int): Pterodactyl Server ID.
        """
        response = self._api_request(
            endpoint='application/servers/{}/reinstall'.format(server_id),
            mode='POST')
        return response

    def rebuild_server(self, server_id):
        """Rebuild the server with the specified internal ID.

        Args:
            server_id(int): Pterodactyl Server ID.
        """
        response = self._api_request(
            endpoint='application/servers/{}/rebuild'.format(server_id),
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
        endpoint = 'application/servers/{}'.format(server_id)
        if force:
            endpoint += '/force'

        response = self._api_request(endpoint=endpoint, mode='DELETE')
        return response

    def list_server_databases(self, server_id, includes=None, params=None):
        """List the database servers assigned to the specified server ID.

        Args:
            server_id(int): Pterodactyl Server ID.
            includes(iter): List of includes, e.g. ('password', 'host')
            params(dict): Extra parameters to pass, e.g. {'per_page': 300}
        """
        endpoint = 'application/servers/{}/databases'.format(server_id)
        response = self._api_request(endpoint=endpoint, includes=includes,
                                     params=params)
        return PaginatedResponse(self, endpoint, response)

    def get_server_database_info(self, server_id, database_id, detail=False,
                                 includes=None, params=None):
        """Get information about the specified database on the specified server.

        Args:
            server_id(int): Pterodactyl Server ID.
            database_id(int): Database ID for specified server.
            detail(bool): If True includes the object type and a nested data
                    structure.
            includes(iter): List of includes, e.g. ('password', 'host')
            params(dict): Extra parameters to pass, e.g. {'per_page': 300}
        """
        endpoint = 'application/servers/{}/databases/{}'.format(server_id,
                                                                database_id)
        response = self._api_request(endpoint=endpoint, includes=includes,
                                     params=params)
        return base.parse_response(response, detail)

    def create_server_database(self, server_id):
        """Create a database for the specified server.

        Args:
            server_id(int): Pterodactyl Server ID.
        """
        response = self._api_request(
            endpoint='application/servers/{}/databases'.format(server_id),
            mode='POST')
        return response

    def delete_server_database(self, server_id, database_id):
        """Delete the specified database for the specified server.

        Args:
            server_id(int): Pterodactyl Server ID.
            database_id(int): Database ID for specified server.
        """
        response = self._api_request(
            endpoint='application/servers/{}/databases/{}'.format(server_id,
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
            endpoint='application/servers/{}/databases/{}'
                     '/reset-password'.format(server_id, database_id),
            mode='POST')
        return response

    def create_server(self, name, user_id, nest_id, egg_id, memory_limit,
                      swap_limit, disk_limit, location_ids=[], port_range=[],
                      environment={}, cpu_limit=0, io_limit=500,
                      database_limit=0, allocation_limit=0, backup_limit=0,
                      docker_image=None, startup_cmd=None, dedicated_ip=False,
                      start_on_completion=True, oom_disabled=True,
                      default_allocation=None, additional_allocations=None,
                      external_id=None, description=None):
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
            backup_limit(int): Maximum number of backups that can be
                    created for this server.
            docker_image(str): Name or URL of the Docker server to use.
                    e.g. quay.io/pterodactyl/core:java-glibc
            startup_cmd(str): Startup command, if specified replaces the
                    egg's default value.
            dedicated_ip(bool): Limit allocations to IPs without any existing
                    allocations.
            start_on_completion(bool): Start server after install completes.
            oom_disabled(bool): Disables OOM-killer on the Docker container.
            default_allocation(int): Specify allocation(s) instead of using the
                    Pterodactyl deployment service.  Uses the allocation's
                    internal ID and not the port number.
            additional_allocations(iter): Additional allocations on top of
                    default_allocation.
            description(str): A description of the server if needed
        """
        if default_allocation is None and not location_ids:
            raise BadRequestError('Must specify either default_allocation or '
                                  'location_ids')

        # Fetch the Egg variables which are required to create the server.
        egg_info = self._api_request(
            endpoint='application/nests/{}/eggs/{}'.format(
                nest_id, egg_id), params={'include': 'variables'})['attributes']
        egg_vars = egg_info['relationships']['variables']['data']

        # Build a dict of environment variables.  Prefer values passed in the
        # environment parameter, otherwise use the default value from the Egg
        # config.
        env_with_defaults = {}
        for var in egg_vars:
            var_name = var['attributes']['env_variable']
            if var_name in environment:
                env_with_defaults[var_name] = environment[var_name]
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
            'external_id': external_id,
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
                'backups': backup_limit
            },
            'environment': env_with_defaults,
            'start_on_completion': start_on_completion,
            'description': description,
        }

        if default_allocation is not None:
            data['allocation'] = {'default': default_allocation,
                                  'additional': additional_allocations}
        elif location_ids:
            data['deploy'] = {'locations': location_ids,
                              'dedicated_ip': dedicated_ip,
                              'port_range': port_range}

        response = self._api_request(endpoint='application/servers',
                                     mode='POST', data=data, json=False)
        return response
    
    def update_server_details(self, server_id, name, user_id, external_id=None, description=None):
        """Updates the details of an existing server.
        
        Modifies an existing server details identified by its Pterodactyl id.
        
        Example of a working set of parameters:
            update_server_details(server_id=10, name='My awesome Server', external_id='some_id2389234', description='This is really an awesome server !'
            
        Args:
            server_id(int): Internal server ID, e.g. 12
            name(str): Name of the server to display in the panel.
            user_id(int): User ID that will own the server.
            external_id(int): Server ID from an external system like WHMCS
            description(str): A description of the server if needed"""

        data = {
            'name': name,
            'user': user_id,
            'external_id': external_id,
            'description': description
        }

        response = self._api_request(
            endpoint='application/servers/{}/details'.format(server_id),
            mode='PATCH', data=data, json=False)
        return response



    def update_server_build(self, server_id, allocation_id, memory_limit=None,
                            swap_limit=None, disk_limit=None, cpu_limit=None,
                            io_limit=None, database_limit=None,
                            allocation_limit=None, backup_limit=None,
                            add_allocations=None,
                            remove_allocations=None, oom_disabled=None):
        """Updates the build configuration for an existing server.

        Modifies an existing server identified by allocation_id and updates
        any parameters that are passed.

        *** WARNING ***
        This endpoint has a lot of requirements and it doesn't always surface
        helpful errors.  Sometimes they're in the panel logs.  I plan to
        automate some of the painful parts so you can specify only the fields
        you want to update, however currently you must satisfy the API's
        requirements by passing in everything.

        Example of a working set of parameters:
            update_server_build(server_id=12, allocation_id=81, 
                    memory_limit=2048, swap_limit=2048, disk_limit=5120, 
                    cpu_limit=100, io_limit=500, database_limit=1, 
                    allocation_limit=2, backup_limit=4, 
                    add_allocations=None, remove_allocations=None, 
                    oom_disabled=True)

        Args:
            server_id(int): Internal server ID, e.g. 12
            allocation_id(int): Base allocation of the server to modify.
            memory_limit(int): Memory limit in MB for the Docker container.  To
                    allow unlimited memory limit set to 0.
            swap_limit(int): Swap limit in MB for the Docker container.  To not
                    assign any swap set to 0.  For unlimited swap set to -1.
            disk_limit(int): Disk limit in MB for the Docker container.  To
                    allow unlimited disk space set to 0.
            cpu_limit(int): CPU limit for the Docker container.  To allow
                    unlimited CPU usage set to 0.  To limit to one core set
                    to 100.  For four cores set to 400.
            io_limit(int): Block IO weight for the Docker container.
                    Must be between 10 and 1000.
            database_limit(int): Maximum number of databases that can be
                    assigned to this server.
            allocation_limit(int): Maximum number of allocations that can be
                    assigned to this server.
            backup_limit(int): Maximum number of backups that can be
                    assigned to this server.
            add_allocations(iter): List of allocation IDs to add to the server.
            remove_allocations(iter): List of allocation IDs to remove from
                    the server.
            oom_disabled(bool): Disables OOM-killer on the Docker container.
        """
        data = {
            'allocation': allocation_id,
            'limits': {},
            'feature_limits': {},
        }

        if memory_limit is not None:
            data['limits']['memory'] = memory_limit
        if swap_limit is not None:
            data['limits']['swap'] = swap_limit
        if disk_limit is not None:
            data['limits']['disk'] = disk_limit
        if cpu_limit is not None:
            data['limits']['cpu'] = cpu_limit
        if io_limit is not None:
            data['limits']['io'] = io_limit
        if database_limit is not None:
            data['feature_limits']['databases'] = database_limit
        if allocation_limit is not None:
            data['feature_limits']['allocations'] = allocation_limit
        if backup_limit is not None:
            data['feature_limits']['backups'] = backup_limit
        if add_allocations is not None:
            data['add_allocations'] = add_allocations
        if remove_allocations is not None:
            data['remove_allocations'] = remove_allocations
        if oom_disabled is not None:
            data['oom_disabled'] = oom_disabled

        response = self._api_request(
            endpoint='application/servers/{}/build'.format(server_id),
            mode='PATCH', data=data, json=False)
        return response

    def update_server_startup(self, server_id, egg_id=None,
                              environment={}, docker_image=None,
                              startup_cmd=None, skip_scripts=None):
        """Updates the startup config for the specified server.

        Modifies the startup config of an existing server replacing any
        specified values.  Unspecified values will not be changed.

        Args:
            egg_id(int): Egg ID to update on the server.
            environment(dict): Key value pairs of Service Variables to set.
                    Every variable from the egg must be set or the API will
                    return an error.  Any keys specified will be overwritten
                    in the existing environment list.  Unspecified keys will
                    not be modified. Extra keys will be dropped.
            docker_image(str): Name or URL of the Docker server to use.
                    e.g. quay.io/pterodactyl/core:java-glibc
            startup_cmd(str): Startup command, if specified replaces the
                    egg's default value.
            skip_scripts(bool): True to skip egg scripts.
        """
        server_info = self._api_request(
            endpoint='application/servers/{}'.format(server_id),
            params={'include': 'variables'})['attributes']
        container = server_info['container']
        current_env = container['environment']
        current_egg = server_info['egg']
        merged_env = {}
        if egg_id is not None and egg_id != current_egg:
            nest_id = server_info['nest']
            egg_info = self._api_request(
                endpoint='application/nests/{}/eggs/{}'.format(nest_id, egg_id),
                params={'include': 'variables'})['attributes']
            egg_vars = egg_info['relationships']['variables']['data']

            # Build a dict of environment variables. Prefer values passed in
            # the environment parameter, then those set in the current env,
            # then finally use the default value from the Egg config.
            for var in egg_vars:
                var_name = var['attributes']['env_variable']
                if var_name in environment:
                    merged_env[var_name] = environment[var_name]
                elif var_name in current_env:
                    merged_env[var_name] = current_env[var_name]
                else:
                    merged_env[var_name] = var['attributes'].get(
                        'default_value')
            if not docker_image:
                docker_image = egg_info.get('docker_image')
            if not startup_cmd:
                startup_cmd = egg_info.get('startup')
        elif environment is not None:
            # If extra values are passed they are silently dropped by the API
            #   could detect attempts to set invalid variables and throw.
            # Also could reduce the contents of current_env down to the
            #   set of variables, there's extra info in here that seems
            #   to not matter if it's set or not.
            merged_env = current_env
            merged_env.update(environment)

        data = {
            'egg': egg_id if egg_id is not None else current_egg,
            'startup': startup_cmd if startup_cmd is not None else container[
                'startup_command'],
            'image': docker_image if docker_image is not None else container[
                'image'],
            # Cant find a way to get the current value for this setting
            #   and this seems better than assuming true or false
            'skip_scripts': skip_scripts if skip_scripts is not None else
            container['installed'] == 1,
            'environment': merged_env
        }

        response = self._api_request(
            endpoint='application/servers/{}/startup'.format(server_id),
            mode='PATCH', data=data, json=False)
        return response
