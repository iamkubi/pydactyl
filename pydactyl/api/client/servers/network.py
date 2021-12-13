from pydactyl.api import base


class Network(base.PterodactylAPI):
    """Pterodactyl Client Server Network API."""

    def list_allocations(self, server_id: str):
        """Retrieves network information for the specified server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
        """
        endpoint = 'client/servers/{}/network/allocations'.format(server_id)
        response = self._api_request(endpoint=endpoint)
        return response

    def assign_allocation(self, server_id: str):
        """Assigns an allocation to the server.

        Automatically assigns a new allocation if auto-assign is enabled on
        the instance.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
        """
        endpoint = 'client/servers/{}/network/allocations'.format(server_id)
        response = self._api_request(endpoint=endpoint, mode='POST')
        return response

    def set_allocation_note(self, server_id: str, allocation_id: int,
                            note: str):
        """Sets the note on an allocation.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            allocation_id(int): Allocation identifier (e.g. 2)
            note(str): Contents of the note
        """
        data = {'notes': note}
        endpoint = 'client/servers/{}/network/allocations/{}'.format(
            server_id, allocation_id)
        response = self._api_request(endpoint=endpoint, mode='POST', data=data)
        return response

    def set_primary_allocation(self, server_id: str, allocation_id: int):
        """Sets the specified allocation as the primary allocation.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            allocation_id(int): Allocation identifier (e.g. 2)
        """
        endpoint = 'client/servers/{}/network/allocations/{}/primary'.format(
            server_id, allocation_id)
        response = self._api_request(endpoint=endpoint, mode='POST')
        return response

    def unassign_allocation(self, server_id: str, allocation_id: int):
        """Deletes the specified non-primary allocation.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            allocation_id(int): Allocation identifier (e.g. 2)
        """
        endpoint = 'client/servers/{}/network/allocations/{}'.format(
            server_id, allocation_id)
        response = self._api_request(endpoint=endpoint, mode='DELETE')
        return response
