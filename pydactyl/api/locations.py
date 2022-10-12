from pydactyl.api.base import PterodactylAPI
from pydactyl.exceptions import BadRequestError
from pydactyl.responses import PaginatedResponse


class Locations(PterodactylAPI):
    """Class for interacting with the Pterdactyl Locations API."""

    def list_locations(self, includes=None):
        """List all locations.

        Args:
            includes(iter): List of includes, e.g. ('servers', 'allocations')
        """
        endpoint = 'application/locations'
        response = self._api_request(endpoint=endpoint, includes=includes)
        return PaginatedResponse(self, endpoint, response)

    def get_location_info(self, location_id, includes=None):
        """Get detailed info for the specified location.

        Args:
            location_id(int): Pterodactyl Location ID.
            includes(iter): List of includes, e.g. ('servers', 'allocations')
        """
        response = self._api_request(
            endpoint='application/locations/{}'.format(location_id),
            includes=includes)
        return response

    def create_location(self, shortcode, description, includes=None):
        """Creates a new location.

        Args:
            shortcode(str): Short identifier between 1 and 60 characters, e.g. us.nyc.lvl3
            description(str): A long description of the location.  Max 255 characters.
            includes(iter): List of includes, e.g. ('servers', 'allocations')
        """
        data = {'shortcode': shortcode, 'description': description}
        response = self._api_request(endpoint='application/locations',
                                     mode='POST', data=data, includes=includes)
        return response

    def edit_location(self, location_id, shortcode=None, description=None,
                      includes=None):
        """Modify an existing location.

        Args:
            location_id(int): Pterodactyl Location ID.
            shortcode(str): Short identifier between 1 and 60 characters, e.g. us.nyc.lvl3
            description(str): A long description of the location.  Max 255 characters.
            includes(iter): List of includes, e.g. ('servers', 'allocations')
        """
        if not shortcode and not description:
            raise BadRequestError(
                'Must specify either shortcode or description for edit_location.')

        data = {}
        if shortcode:
            data['shortcode'] = shortcode
        if description:
            data['description'] = description

        response = self._api_request(
            endpoint='application/locations/{}'.format(location_id),
            mode='PATCH', data=data, includes=includes)
        return response

    def delete_location(self, location_id, includes=None):
        """Delete an existing location.

        Args:
            location_id(int): Pterodactyl Location ID.
            includes(iter): List of includes, e.g. ('servers', 'allocations')
        """
        response = self._api_request(
            endpoint='application/locations/{}'.format(location_id),
            mode='DELETE', includes=includes)
        return response
