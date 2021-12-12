from pydactyl.api import base


class Schedules(base.PterodactylAPI):
    """Pterodactyl Client Server Databases API."""

    def list_schedules(self, server_id: str):
        """List all schedules for a server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
        """
        endpoint = 'client/servers/{}/schedules'.format(server_id)
        response = self._api_request(endpoint=endpoint)
        return response

    def create_schedule(self):
        """TODO"""
        pass

    def get_schedule_details(self, schedule_id):
        """"TODO"""
        pass

    def update_schedule(self, schedule_id):
        """TODO"""
        pass

    def delete_schedule(self, schedule_id):
        """TODO"""
        pass

    def create_task(self, schedule_id):
        """TODO"""
        pass

    def update_task(self, schedule_id):
        """TODO"""
        pass

    def delete_task(self, schedule_id):
        """TODO"""
        pass
