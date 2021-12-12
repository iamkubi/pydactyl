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

    def assign_allocation(self):
        """TODO"""
        pass

    def set_allocation_note(self):
        """TODO"""
        pass

    def set_primary_allocation(self):
        """TODO"""
        pass

    def unassign_allocation(self):
        """TODO"""
        pass
