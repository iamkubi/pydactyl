from pyteroapi import Pydactyl


class Client(Pydactyl):
    """Class for interacting with the Pterdactyl Client API."""

    def __init__(self):
        super(Pydactyl).__init__()

    def list_servers(self):
        """List all servers the client has access to."""

    def get_server(self, id):
        """Get information for the specified server.

        Args:
            id(str): UUID of a server
        """

    def get_server_utilization(self, id):
        """Get resource utilization information for the specified server.

        Args:
            id(str): UUID of a server
        """

    def send_console_command(self, id, cmd):
        """Sends a console command to the specified server.

        The server must be online, otherwise API will return a HTTP 412 error.
        If successful, there will be an empty response body.

        Args:
            id(str): UUID of a server
            cmd(str): Console command to send to the server
        """

    def send_power_action(self, id, signal):
        """Sends a console command to the specified server.

        The server must be online, otherwise API will return a HTTP 412 error.
        If successful, there will be an empty response body.

        Args:
            id(str): UUID of a server
            signal(str): Power signal to send to the server.  Possible options include:
                start - Sends the startup command to the server.
                stop - Sends the stop command to the server.
                restart - Stops the server then immediately starts it.
                kill - Instantly ends all processes and marks the server as stopped.
                       The kill signal can corrupt server files and should only be used as a last resort.
        """
