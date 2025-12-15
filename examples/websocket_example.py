import argparse
import datetime
from pydactyl import PterodactylClient


parser = argparse.ArgumentParser(description='Pterodactyl Websocket Example')
parser.add_argument('url', help='Panel URL')
parser.add_argument('api_key', help='Client API Key')
parser.add_argument('server_id', help='Server UUID')
    
args = parser.parse_args()
api = PterodactylClient(args.url, args.api_key)

with api.client.servers.get_websocket_client(args.server_id) as ws:
      for msg in ws.listen():
          print('{} - {}'.format(datetime.datetime.now(), msg))