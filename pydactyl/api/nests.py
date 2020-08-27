from pydactyl.api.base import PterodactylAPI
from pydactyl.responses import PaginatedResponse


class Nests(PterodactylAPI):
    """Class for interacting with the Pterdactyl Nests API."""

    def list_nests(self):
        """List all nests."""
        endpoint = 'application/nests'
        response = self._api_request(endpoint=endpoint)
        return PaginatedResponse(self, endpoint, response)

    def get_nest_info(self, nest_id):
        """Get detailed info for the specified nest.

        Args:
            nest_id(int): Pterodactyl Nest ID.
        """
        response = self._api_request(endpoint='application/nests/%s' % nest_id)
        return response

    def get_eggs_in_nest(self, nest_id):
        """Get detailed info for the specified nest.

        Args:
            nest_id(int): Pterodactyl Nest ID.
        """
        response = self._api_request(
            endpoint='application/nests/%s/eggs' % nest_id)
        return response

    def get_egg_info(self, nest_id, egg_id):
        """Get detailed info for the specified egg.

        Args:
            nest_id(int): Pterodactyl Nest ID.
            egg_id(int): Pterodactyl Egg ID.
        """
        response = self._api_request(
            endpoint='application/nests/%s/eggs/%s' % (nest_id, egg_id))
        return response
