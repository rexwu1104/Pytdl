import orjson as json
from collections.abc import Callable
from typing import (
	Dict,
	List,
	Union
)

__all__ = (
	'Parser'
)

JSON = Dict[str, Union[str, List, Dict]]

def dp(d : int) -> str:
	result = ''
	h = d // 3600
	m = (d - h * 3600) // 60
	s = (d - h * 3600) - m * 60

	if h < 10:
		result += '0' + str(h)
	else:
		result += str(h)
	result += ':'
	if m < 10:
		result += '0' + str(m)
	else:
		result += str(m)
	result += ':'
	if s < 10:
		result += '0' + str(s)
	else:
		result += str(s)

	return result

class Parser:
	scriptData = None
	def __init__(self, type : str):
		self.type : str = type
		self.result : list = []
        
		if type not in [
			'search',
			'video',
			'playlist',
			'spotifyTrack',
			'spotifyPlaylist',
			'spotifyAlbum'
		]: raise Exception('%s is a invalid type' % type)
            
		self.cut : Callable = {
			'search': self.searchCut,
			'video': self.videoCut,
			'playlist': self.playlistCut,
			'spotifyTrack': self.spotifyTrackCut,
			'spotifyPlaylist': self.spotifyPlaylistCut,
			'spotifyAlbum': self.spotifyAlbumCut
		}[self.type]

		if self.type.startswith('spotify'):
			self.load : Callable = self.loadSpotify
		else:
			self.load : Callable = self.loadYoutube
        
	def loadYoutube(self, data : str) -> None:
		self.scriptData = json.loads(
			data \
			.strip('var ytInitialData = ') \
			.strip(';')
		)

	def loadSpotify(self, data : JSON) -> None:
		if 'album' in data:
			result = data
		elif type(data) is list:
			result = []
			for idx in range(len(data)):
				t = data[idx]
				if 'album' not in t and 'artists' in t:
					t['album'] = t
				if 'track' not in t and 'album' in t:
					t['track'] = t
				if 'track' in t and t['track'] is not None:
					track = t['track']
					result.append(track)
		self.scriptData = result
        
	def searchCut(self) -> None:
		if self.scriptData is None:
			raise Exception('data is not load')
            
		data = self.scriptData
		for result in data['contents'] \
											['twoColumnSearchResultsRenderer'] \
											['primaryContents'] \
											['sectionListRenderer'] \
											['contents'][0] \
											['itemSectionRenderer'] \
											['contents']:
			
			if result.get('videoRenderer') is None:
				continue
			obj : dict = result['videoRenderer']

			self.result.append({
				'id': obj['videoId'],
				'title': obj['title']['runs'][0]['text'],
				'thumbnail': obj['thumbnail']['thumbnails'],
				'length': obj['lengthText']['simpleText'] \
					if 'lengthText' in obj else 'STREAMING',
				'author': obj['shortBylineText']['runs'][0]['text']
			})

	def videoCut(self) -> None:
		if self.scriptData is None:
			raise Exception('data is not load')
            
		data = self.scriptData
		result = data['contents'] \
								 ['twoColumnWatchNextResults'] \
								 ['secondaryResults'] \
								 ['secondaryResults'] \
								 ['results'][1]

		obj : dict = result['compactVideoRenderer']

		self.result.append({
			'id': obj['videoId'],
			'title': obj['title']['simpleText'],
			'thumbnail': obj['thumbnail']['thumbnails'],
			'length': obj['lengthText']['simpleText'] \
				if 'lengthText' in obj else 'STREAMING',
			'author': obj['shortBylineText']['runs'][0]['text']
		})

	def playlistCut(self) -> None:
		if self.scriptData is None:
			raise Exception('data is not load')
            
		data = self.scriptData
		for result in data['contents'] \
											['twoColumnBrowseResultsRenderer'] \
											['tabs'][0] \
											['tabRenderer'] \
											['content'] \
											['sectionListRenderer'] \
											['contents'][0] \
											['itemSectionRenderer'] \
											['contents'][0] \
											['playlistVideoListRenderer'] \
											['contents']:
			
			if result.get('playlistVideoRenderer') is None:
				continue
			obj : dict = result['playlistVideoRenderer']

			self.result.append({
				'id': obj['videoId'],
				'title': obj['title']['runs'][0]['text'],
				'thumbnail': obj['thumbnail']['thumbnails'],
				'length': obj['lengthText']['simpleText'] \
					if 'lengthText' in obj else 'STREAMING',
				'author': obj['shortBylineText']['runs'][0]['text']
			})

	def spotifyAlbumCut(self) -> None:
		if self.scriptData is None:
			raise Exception('data is not load')

		tracks = self.scriptData
		for track in tracks:
			duration = track['duration_ms'] // 1000
			self.result.append({
				'id': track['id'],
				'title': track['name'],
				'thumbnail': [] or track['album']['images'],
				'length': dp(duration),
				'author': [] or track['artists']
			})

	def spotifyTrackCut(self) -> None:
		if self.scriptData is None:
			raise Exception('data is not load')

		track = self.scriptData
		duration = track['duration_ms'] // 1000
		self.result.append({
			'id': track['id'],
			'title': track['name'],
			'thumbnail': track['album']['images'],
			'length': dp(duration),
			'author': [] or track['artists']
		})

	def spotifyPlaylistCut(self) -> None:
		if self.scriptData is None:
			raise Exception('data is not load')

		tracks = self.scriptData
		for track in tracks:
			duration = track['duration_ms'] // 1000
			self.result.append({
				'id': track['id'],
				'title': track['name'],
				'thumbnail': track['album']['images'],
				'length': dp(duration),
				'author': [] or track['artists']
			})