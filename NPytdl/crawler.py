from aiohttp import ClientSession as cli
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from typing import (
	Dict,
	List,
	Union
)

from base64 import b64decode
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials as SCC

client_id = \
	b64decode(b'N2U0ZDI2ZDAyMjNlNDkxNzgzMmI1NDIxNmZmODE2OWU=') \
	.decode()
client_secret = \
	b64decode(b'NTc0YWViNzY2MmMxNDNiM2EwMThjODYwZDI5M2I4ZmU=') \
	.decode()

sp = spotipy.Spotify(auth_manager=SCC(
	client_id = client_id,
	client_secret = client_secret
))

__all__ = (
	'get',
	'spotifyGet'
)

JSON = Dict[str, Union[str, List, Dict]]

from .dataParser import Parser

async def fetch(client : cli, url : str) -> str:
	async with client.get(url) as res:
		if res.status >= 200 or res.status < 300:
			return await res.text()
		else:
			raise Exception('Response is not success.')
            
async def get(url : str, parser : Parser) -> JSON:
	async with cli() as client:
		html : str = await fetch(client, url)
		scripts : list = [s.text for s in bs(
			html,
			"html.parser"
		).find_all('script')]

		parser.load(
			sorted(
				scripts
				, key = lambda t: t.find("var ytInitialData = ")
			)[-1]
		)  
		parser.cut()
		return parser.result

async def spotifyGet(url : str, parser : Parser) -> JSON:
	p = urlparse(url)
	if p.path.startswith('/track'):
		result : JSON = sp.track(p[2].split('/')[2])
	elif p.path.startswith('/playlist'):
		result : JSON = sp.playlist(p[2].split('/')[2]) \
			['tracks']['items']
	elif p.path.startswith('/album'):
		result : JSON = sp.album_tracks(p[2].split('/')[2]) \
			['items']
	else:
		result : JSON = sp.search(q=url, limit=12)
		result = result['tracks']['items']
			
	parser.load(
		result
	)
	parser.cut()
	return parser.result