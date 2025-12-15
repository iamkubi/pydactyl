import argparse
import asyncio
import datetime
from pydactyl import AsyncPterodactylClient


async def main(args):
    async with AsyncPterodactylClient(args.url, args.api_key) as api:
        ws_client = await api.client.servers.get_websocket_client(args.server_id)
        async with ws_client as ws:
            async for msg in ws.listen():
                print('{} - {}'.format(datetime.datetime.now(), msg))


parser = argparse.ArgumentParser(description='Async Pterodactyl Websocket Example')
parser.add_argument('url', help='Panel URL')
parser.add_argument('api_key', help='Client API Key')
parser.add_argument('server_id', help='Server UUID')

args = parser.parse_args()
asyncio.run(main(args))