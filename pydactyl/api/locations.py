from pydactyl.api.base import PterodactylAPI
from pydactyl.exceptions import BadRequestError
from pydactyl.responses import PaginatedResponse


class Locations(PterodactylAPI):
    """Class for interacting with the Pterdactyl Locations API."""

    def list_locations(self):
        """List all locations."""
        endpoint = 'application/locations'
        response = self._api_request(endpoint=endpoint)
        return PaginatedResponse(self, endpoint, response)

    def get_location_info(self, location_id):
        """Get detailed info for the specified location.

        Args:
            location_id(int): Pterodactyl Location ID.
        """
        response = self._api_request(
            endpoint='application/locations/%s' % location_id)
        return response

    def create_location(self, shortcode, description):
        """Creates a new location.

        Args:
            shortcode(str): Short identifier between 1 and 60 characters, e.g. us.nyc.lvl3
            description(str): A long description of the location.  Max 255 characters.
        """
        data = {'shortcode': shortcode, 'description': description}
        response = self._api_request(endpoint='application/locations',
                                     mode='POST', data=data)
        return response

    def edit_location(self, location_id, shortcode=None, description=None):
        """Modify an existing location.

        Args:
            location_id(int): Pterodactyl Location ID.
            shortcode(str): Short identifier between 1 and 60 characters, e.g. us.nyc.lvl3
            description(str): A long description of the location.  Max 255 characters.
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
            endpoint='application/locations/%s' % location_id, mode='PATCH',
            data=data)
        return response

    def delete_location(self, location_id):
        """Delete an existing location.

        Args:
            location_id(int): Pterodactyl Location ID.
        """
        response = self._api_request(
            endpoint='application/locations/%s' % location_id, mode='DELETE')
        return response
