import aiohttp
import json
import logging


class AsyncWebsocketClient:
    """Helper class for interacting with a Pterodactyl server's websocket.

    This class provides methods to connect, authenticate, send commands,
    and receive events from the server console.
    """

    def __init__(self, url, token, session=None, token_refresher=None):
        """Initialize the Websocket client.

        Args:
            url (str): The websocket URL to connect to.
            token (str): The authentication token.
            session (aiohttp.ClientSession, optional): Existing aiohttp session.
            token_refresher (function, optional): Async function to refresh the token.
        """
        self._url = url
        self._token = token
        self._session = session
        self._token_refresher = token_refresher
        self._ws = None
        self._logger = logging.getLogger(__name__)

    async def connect(self):
        """Connect to the websocket."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()

        self._ws = await self._session.ws_connect(self._url)
        await self.authenticate()

    async def close(self):
        """Close the websocket connection."""
        if self._ws:
            await self._ws.close()

        # Only close the session if we created it? 
        # For now, let's assume we clean up if we created it, 
        # but the common use case is passing a session in.
        # Actually, in async_base, we often manage the session.
        pass

    async def authenticate(self):
        """Authenticate with the server."""
        await self.send("auth", [self._token])

    async def send(self, event: str, args = None):
        """Send an event to the server.

        Args:
            event (str): The event name (e.g., 'auth', 'send', 'set state').
            args (list, optional): Arguments for the event.
        """
        if not self._ws:
            raise RuntimeError("Websocket is not connected.")

        payload = {"event": event, "args": args or []}
        await self._ws.send_json(payload)

    async def send_command(self, command: str):
        """Send a console command to the server.

        Args:
            command (str): The command string.
        """
        await self.send("send", [command])

    async def send_power_action(self, signal: str):
        """Send a power action to the server.

        Args:
            signal (str): The power state (start, stop, restart, kill).
        """
        await self.send("set state", [signal])

    async def request_logs(self):
        """Request server logs."""
        await self.send("send logs")

    async def request_stats(self):
        """Request server stats."""
        await self.send("send stats")

    async def listen(self, events = (), exclude_events = ()):
        """Async generator that yields messages from the server.
        
        Args:
            events (list[str], optional): The events to listen for.
            exclude_events (list[str], optional): The events to exclude.
            
        Yields:
             dict: The parsed JSON message from the server.
        """
        if not self._ws:
            raise RuntimeError("Websocket is not connected.")

        async for msg in self._ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                    if data['event'] == 'token expiring':
                        if self._token_refresher:
                            try:
                                response = await self._token_refresher()
                                self._token = response['data']['token']
                                await self.authenticate()
                                self._logger.info("Websocket token refreshed.")
                            except Exception as e:
                                self._logger.error("Failed to refresh websocket token: %s", e)

                    if (events and data['event'] not in events or
                        exclude_events and data['event'] in exclude_events):
                        continue
                    yield data
                except ValueError:
                    self._logger.warning("Received non-JSON message: %s", msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                self._logger.error("Websocket connection closed with exception %s",
                                   self._ws.exception())
                break

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
