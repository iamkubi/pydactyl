from pydactyl.api.base import PterodactylAPI
from pydactyl.responses import PaginatedResponse


class Nests(PterodactylAPI):
    """Class for interacting with the Pterdactyl Nests API."""

    def list_nests(self, *include):
        """List all nests.

        Args:
            include(*string): Zero or more include options (eggs, servers)
        """
        params = None if not include else {'include': ','.join(include)}
        endpoint = 'application/nests'
        response = self._api_request(endpoint=endpoint, params=params)
        return PaginatedResponse(self, endpoint, response)

    def get_nest_info(self, nest_id, *include):
        """Get detailed info for the specified nest.

        Args:
            nest_id(int): Pterodactyl Nest ID.
            include(*string): Zero or more include options (eggs, servers)
        """
        params = None if not include else {'include': ','.join(include)}
        response = self._api_request(endpoint='application/nests/%s' % nest_id,
                                     params=params)
        return response

    def get_eggs_in_nest(self, nest_id, *include):
        """Get detailed info for the specified nest.

        Args:
            nest_id(int): Pterodactyl Nest ID.
            include(*string): Zero or more include options (nest, servers, config, script, variables)
        """
        params = None if not include else {'include': ','.join(include)}
        response = self._api_request(
            endpoint='application/nests/%s/eggs' % nest_id,
            params=params)
        return response

    def get_egg_info(self, nest_id, egg_id, *include):
        """Get detailed info for the specified egg.

        Args:
            nest_id(int): Pterodactyl Nest ID.
            egg_id(int): Pterodactyl Egg ID.
            include(*string): Zero or more include options (nest, servers, config, script, variables)
        """
        params = None if not include else {'include': ','.join(include)}
        response = self._api_request(
            endpoint='application/nests/%s/eggs/%s' % (nest_id, egg_id),
            params=params)
        return response
