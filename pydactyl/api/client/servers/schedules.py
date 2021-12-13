from pydactyl.api import base
from pydactyl.constants import SCHEDULE_ACTIONS
from pydactyl.exceptions import BadRequestError


def check_schedule_action_valid(action):
    if action not in SCHEDULE_ACTIONS:
        raise BadRequestError(
            'Invalid schedule action sent({}), must be one of: {}'.format(
                action, SCHEDULE_ACTIONS))


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

    def create_schedule(self, server_id: str, name: str, minute: str,
                        hour: str, day_of_week: str, day_of_month: str,
                        is_active: bool = True):
        """Creates a new schedule for the specified server.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            name(str): Friendly name for the schedule
            minute(str): Value for Cron minute field
            hour(str): Value for Cron hour field
            day_of_week(str): Value for Cron day_of_week field
            day_of_month(str): Value for Cron day_of_month field
            is_active(bool): False to create the schedule as disabled
        """
        data = {'name': name, 'minute': minute, 'hour': hour,
                'day_of_week': day_of_week, 'day_of_month': day_of_month,
                'is_active': is_active}
        endpoint = 'client/servers/{}/schedules'.format(server_id)
        response = self._api_request(endpoint=endpoint, mode='POST', data=data)
        return response

    def get_schedule_details(self, server_id: str, schedule_id: int):
        """Retrieves the specified schedule.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            schedule_id(int): Schedule identifier (e.g. 2)
        """
        endpoint = 'client/servers/{}/schedules/{}'.format(server_id,
                                                           schedule_id)
        response = self._api_request(endpoint=endpoint)
        return response

    def update_schedule(self, server_id: str, schedule_id: int, name: str,
                        minute: str, hour: str, day_of_week: str,
                        day_of_month: str, is_active: bool = True):
        """Updates the specified schedule.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            schedule_id(int): Schedule identifier (e.g. 2)

            name(str): Friendly name for the schedule
            minute(str): Value for Cron minute field
            hour(str): Value for Cron hour field
            day_of_week(str): Value for Cron day_of_week field
            day_of_month(str): Value for Cron day_of_month field
            is_active(bool): False to create the schedule as disabled
        """
        data = {'name': name, 'minute': minute, 'hour': hour,
                'day_of_week': day_of_week, 'day_of_month': day_of_month,
                'is_active': is_active}
        endpoint = 'client/servers/{}/schedules/{}'.format(server_id,
                                                           schedule_id)
        response = self._api_request(endpoint=endpoint, mode='POST', data=data)
        return response

    def delete_schedule(self, server_id: str, schedule_id: int):
        """Deletes the specified schedule.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            schedule_id(int): Schedule identifier (e.g. 2)
        """
        endpoint = 'client/servers/{}/schedules/{}'.format(server_id,
                                                           schedule_id)
        response = self._api_request(endpoint=endpoint, mode='DELETE')
        return response

    def create_task(self, server_id: str, schedule_id: int, action: str,
                    payload: str, time_offset: str = '0'):
        """Creates a new task on the specified schedule.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            schedule_id(int): Schedule identifier (e.g. 2)
            action(str): Type of action to use
            payload(str): Payload to send for the action
            time_offset(str): Offset in seconds
        """
        check_schedule_action_valid(action)
        data = {'action': action, 'payload': payload,
                'time_offset': time_offset}
        endpoint = 'client/servers/{}/schedules/{}/tasks'.format(server_id,
                                                                 schedule_id)
        response = self._api_request(endpoint=endpoint, mode='POST', data=data)
        return response

    def update_task(self, server_id: str, schedule_id: int, task_id: int,
                    action: str, payload: str, time_offset: str = '0'):
        """Updates the specified task.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            schedule_id(int): Schedule identifier (e.g. 2)
            task_id(int): Task identifier (e.g. 4)
            action(str): Type of action to use
            payload(str): Payload to send for the action
            time_offset(str): Offset in seconds
        """
        check_schedule_action_valid(action)
        data = {'action': action, 'payload': payload,
                'time_offset': time_offset}
        endpoint = 'client/servers/{}/schedules/{}/tasks/{}'.format(
            server_id, schedule_id, task_id)
        response = self._api_request(endpoint=endpoint, mode='POST', data=data)
        return response

    def delete_task(self, server_id: str, schedule_id: int, task_id: int):
        """Deletes the specified task.

        Args:
            server_id(str): Server identifier (abbreviated UUID)
            schedule_id(int): Schedule identifier (e.g. 2)
            task_id(int): Task identifier (e.g. 4)
        """
        endpoint = 'client/servers/{}/schedules/{}/tasks/{}'.format(
            server_id, schedule_id, task_id)
        response = self._api_request(endpoint=endpoint, mode='DELETE')
        return response
