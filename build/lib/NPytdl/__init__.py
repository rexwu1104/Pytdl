import youtube_dl
from typing import List
from aiohttp import ClientSession
import re
import json
import asyncio

class UnKnownError(Exception):
	pass

class __Logger:
	def debug(self, msg):
		pass

	def warning(self, msg):
		pass

	def error(self, msg):
		pass

def __hook(data):
	if data["status"] == "finished":
		print("downing successful.")

class Stream:
	def __init__(self, url : str):
		self.__url = url

	def download(self, path : str = "./"):
		ydl_opts = {
    	'format': 'bestaudio/best',
    	'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    	}],
    	'logger': globals()["__Logger"](),
    	'progress_hooks': [globals()["__hook"]],
			'outtmpl': path if path != "./" else "./%(id)s.mp3",
		}

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.extract_info(self.__url, download=True)

class Song:
	ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192',
    }],
    'logger': globals()["__Logger"](),
    'progress_hooks': [globals()["__hook"]]
	}
	
	def __duration(self, seconds : int):
		h, m, s = (seconds//3600, seconds//60-(seconds//3600)*60, seconds%60)
		result = f"{h if h > 10 else f'0{h}'}:{m if m > 10 else f'0{m}'}:{s if s > 10 else f'0{s}'}"
		if (result := result.split(":"))[0] == "00":
			return result[1] + ":" + result[2]
		return ":".join(result)

	async def __get(self, url : str):
		with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
			return ydl.extract_info(url, download=False)

	async def create(self):
		data = await self.__data
		if type(data) == dict:
			self.duration = self.__duration(data["duration"])
			self.id = data["id"]
			self.thumbnail = data["thumbnail"]
			self.video_url = data["webpage_url"]
			self.voice_url = data["url"]
			self.title = data["title"]
			self.stream = Stream(data["webpage_url"])
		elif len(data) == 1:
			data = data[0]
			self.duration = self.__duration(data["duration"])
			self.id = data["id"]
			self.thumbnail = data["thumbnail"]
			self.video_url = data["webpage_url"]
			self.voice_url = data["url"]
			self.title = data["title"]
			self.stream = Stream(data["webpage_url"])
		else:
			self.Songs = [Song(data[i]) for i in range(len(data))]

	def __init__(self, url_or_urls_or_data):
		if type(url_or_urls_or_data) == str and not re.fullmatch(r'https://w{0,3}\.?youtu(\.be/|be\.com/watch\?v=)[a-zA-Z0-9]*', url_or_urls_or_data):
			raise TypeError("url is not a youtube video url")
		if type(url_or_urls_or_data) == str:
			self.__data = asyncio.gather(*[asyncio.create_task(self.__get(url_or_urls_or_data))])
		elif type(url_or_urls_or_data) == list:
			self.__data = asyncio.gather(*[asyncio.create_task(self.__get(url)) for url in url_or_urls_or_data])
		else:
			data = url_or_urls_or_data
			self.duration = self.__duration(data["duration"])
			self.id = data["id"]
			self.thumbnail = data["thumbnail"]
			self.video_url = data["webpage_url"]
			self.voice_url = data["url"]
			self.title = data["title"]
			self.stream = Stream(data["webpage_url"])

class SongList:
	ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192',
    }],
    'logger': globals()["__Logger"](),
    'progress_hooks': [globals()["__hook"]]
	}

	def __get(self, list_url : str):
		with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
			return ydl.extract_info(list_url, False)

	async def create(self):
		self.songs = Song(await self.__data)

	def __init__(self, list_url : str):
		if not re.fullmatch(r'https://www\.youtube\.com/(watch\?v=[a-zA-z0-9_-]*&|playlist\?)list=[a-zA-Z0-9_-]*', list_url):
			raise TypeError("url is not a youtube list url")
		ydl = Pytdl()
		self.__data = ydl.searchList(list_url.split("=")[-1])

class Pytdl:
	__api_key = "AIzaSyB5k7wA5-9inJlw5lKIzlTYduTzZekpgjc"
	__head = "https://www.googleapis.com/youtube/v3/"
	__Search = "search?part=snippet&q={}&key={}&type=video" #搜尋
	# __Commanets = "commentThreads?part=snippet,contentDetails,replies&videoId={}&key={}" #留言
	__PlayList = "playlistItems?part=snippet,contentDetails&playlistId={}&key={}" #播放清單
	# __Channel = "channels?part=snippet,contentDetails&id={}&key={}" #頻道
	__Video = "videos?id={}&key={}&part=snippet,contentDetails" #影片
	__NextPage = "&pageToken={}" #下一頁
	__max = "&maxResults={}"

	async def __duration(self, time_str : str):
		time_str = time_str.strip("PT").strip("S")
		if time_str.find("H") != -1 and time_str.find("M") == -1:
			time_str = time_str.replace("H", ":00:")
		else:
			time_str = time_str.replace("H", ":").replace("M", ":")
			if int("00" + (time_str := time_str.split(":"))[1]) < 10:
				time_str[1] = "0" + time_str[1]
				if time_str[1] == "0":
					time_str += "0"
				time_str = ":".join(time_str)
		if type(time_str) == list:
			time_str = ":".join(time_str)
		return time_str

	async def __fetch(self, link : str, session : ClientSession):
		async with session.get(link) as response:
			html_body = await response.text()
			return html_body

	async def __video(self, id_list : List[str]):
		async with ClientSession() as session:
			idData = await self.__fetch(self.__head + self.__Video.format(",".join(id_list), self.__api_key), session)
			idData = json.loads(idData)
		results = []
		for item in idData["items"]:
			thumbnails = item["snippet"]["thumbnails"]
			results.append({
				"id": item["id"],
				"title": item["snippet"]["title"],
				"thumbnail": [thumbnails[i]["url"] for i in thumbnails],
				"length": await self.__duration(item["contentDetails"]["duration"])
			})
		return results

	async def songList(self, query : str, size : int = 12):
		async with ClientSession() as session:
			songData = json.loads(await self.__fetch(self.__head + self.__Search.format(query, self.__api_key) + self.__max.format(size), session))
		return await self.__video([item["id"]["videoId"] for item in songData["items"]])

	async def searchList(self, listId : str):
		async with ClientSession() as session:
			listData = await self.__fetch(self.__head + self.__PlayList.format(listId, self.__api_key) + self.__max.format(40), session)
			listData = json.loads(listData)
		return ["https://youtu.be/" + item["contentDetails"]["videoId"] for item in listData["items"]]

	async def songs(self, querys : List[str]):
		async with ClientSession() as session:
			searchList = [asyncio.create_task(self.__fetch(self.__head + self.__Search.format(query, self.__api_key) + self.__max.format(12), session)) for query in querys]
			data = await asyncio.gather(*searchList)
			data = [await self.__video(Ids) for Ids in [list(map(lambda x: x["id"]["videoId"], items)) for items in [json.loads(S)["items"] for S in data]]]
			return data

	async def info(self, url : str):
		try:
			return Song(url)
		except TypeError:
			return SongList(url)
		except:
			raise UnKnownError("not a correct url.")