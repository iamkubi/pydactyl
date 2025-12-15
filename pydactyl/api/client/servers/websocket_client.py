import json
import logging
import websocket

class WebsocketClient:
    """Helper class for interacting with a Pterodactyl server's websocket (Sync).

    This class provides methods to connect, authenticate, send commands,
    and receive events from the server console.
    """

    def __init__(self, url, token, token_refresher=None):
        """Initialize the Websocket client.

        Args:
            url (str): The websocket URL to connect to.
            token (str): The authentication token.
            token_refresher (callable, optional): Function to refresh the token.
        """
        self._url = url
        self._token = token
        self._token_refresher = token_refresher
        self._ws = None
        self._logger = logging.getLogger(__name__)

    def connect(self):
        """Connect to the websocket."""
        self._ws = websocket.create_connection(self._url)
        self.authenticate()

    def close(self):
        """Close the websocket connection."""
        if self._ws:
            self._ws.close()

    def authenticate(self):
        """Authenticate with the server."""
        self.send("auth", [self._token])

    def send(self, event, args=None):
        """Send an event to the server.

        Args:
            event (str): The event name (e.g., 'auth', 'send', 'set state').
            args (list, optional): Arguments for the event.
        """
        if not self._ws:
            raise RuntimeError("Websocket is not connected.")
        
        payload = {"event": event, "args": args or []}
        self._ws.send(json.dumps(payload))

    def send_command(self, command):
        """Send a console command to the server.

        Args:
            command (str): The command string.
        """
        self.send("send command", [command])

    def send_power_action(self, signal: str):
        """Send a power action to the server.

        Args:
            signal (str): The power state (start, stop, restart, kill).
        """
        self.send("set state", [signal])

    def get_status(self):
        """Request server power state."""
        self.send("status")

    def get_logs(self):
        """Request server console output."""
        self.send("console output")

    def get_stats(self):
        """Request server stats, e.g. CPU, memory, disk usage."""
        self.send("stats")

    def listen(self, events = (), exclude_events = ()):
        """Generator that yields events from the server.
        
        Args:
            events (list[str], optional): The events to listen for.
            exclude_events (list[str], optional): The events to exclude.

        Yields:
             dict: The parsed JSON message from the server.
        """
        if not self._ws:
            raise RuntimeError("Websocket is not connected.")

        while True:
            try:
                message = self._ws.recv()
                if not message:
                    break
                
                try:
                    data = json.loads(message)
                    if data['event'] == 'token expiring':
                        if self._token_refresher:
                            try:
                                response = self._token_refresher()
                                self._token = response['data']['token']
                                self.authenticate()
                                self._logger.info("Websocket token refreshed.")
                            except Exception as e:
                                self._logger.error("Failed to refresh websocket token: %s", e)

                    if (events and data['event'] not in events or 
                        exclude_events and data['event'] in exclude_events):
                        continue
                    yield data
                except ValueError:
                    self._logger.warning("Received non-JSON message: %s", message)
            except websocket.WebSocketConnectionClosedException:
                self._logger.info("Websocket connection closed.")
                break
            except Exception as e:
                self._logger.error("Error receiving message: %s", e)
                break

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
