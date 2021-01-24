import os
import sys
import pafy
import json
import subprocess
import urllib as u
import platform

path = [i if i.endswith("site-packages") else None for i in sys.path]

system = platform.system()

if system == "Windows":
  os.system("icacls C://*")
elif system == "Linux" or system == "Darwin":
  os.system("chmod u+x /home/*")

class Pytdl:
  def __init__(self):
    self.__nowData = {}
    self.__prevData = {}
    self.__noNeed = [
      "_ydl_info",
      "_ydl_opts",
      "version",
      "callback",
      "_have_basic",
      "_have_gdata",
      "_username",
      "_streams",
      "_oggstreams",
      "_m4astreams",
      "_allstreams",
      "_videostreams",
      "_keywords",
      "_bigthumb",
      "_bigthumbhd",
      "_mix_pl",
      "expiry"
    ]
    pafy.set_api_key("AIzaSyBxmDSkfH8mSQCGKe1PiKaOdohHI0BeLDg")

  def setup(self):
    pafy.set_api_key("AIzaSyBxmDSkfH8mSQCGKe1PiKaOdohHI0BeLDg")

  async def __datatry(self, ex, *args):
    a=True
    times = 0
    while a:
      if times == 3:
        raise Exception("Can't get this data.")
      try:
        data = await ex(*args)
        a = False
      except TypeError:
        data = ex(*args)
        a = False
      except:
        times += 1
        continue
    return data
  
  async def __search(self, content : str):
    for i in path:
      if i is None:
        continue
      else:
        try:
          data = subprocess.check_output(f'{i}/NPytdl/search https://www.youtube.com/results?search_query={u.parse.quote(content).replace("%20", "+")}', shell=True).decode("utf-8")
        except:
          continue
    data = json.loads(data)
    result = []
    for i in data:
      if "videoRenderer" in i:
        result.append({
          "id": i["videoRenderer"]["videoId"],
          "title": i["videoRenderer"]["title"]["runs"][0]["text"],
          "thumbnail": i["videoRenderer"]["thumbnail"]["thumbnails"][0]["url"],
          "length": "0:00"
        })
        if "lengthText" in i["videoRenderer"]:
          result[-1]["length"] = i["videoRenderer"]["lengthText"]["simpleText"]
    return result

  async def searchList(self, list_id : str):
    for i in path:
      if i is None:
        continue
      else:
        try:
          data = subprocess.check_output(f'{i}/NPytdl/search https://www.youtube.com/playlist?list={list_id} list', shell=True).decode("utf-8")
        except:
          continue
    data = json.loads(data)
    result = []
    for i in data:
      if "playlistVideoRenderer" in i:
        if "videoId" in i["playlistVideoRenderer"]:
          result.append(f'https://youtu.be/{i["playlistVideoRenderer"]["videoId"]}')
    return result    

  async def __getPafy(self, url : str):
    self.__nowData = {}
    self.__prevData = {}
    self.__noNeed = [
      "_ydl_info",
      "_ydl_opts",
      "version",
      "callback",
      "_have_basic",
      "_have_gdata",
      "_username",
      "_streams",
      "_oggstreams",
      "_m4astreams",
      "_allstreams",
      "_videostreams",
      "_keywords",
      "_bigthumb",
      "_bigthumbhd",
      "_mix_pl",
      "expiry"
    ]
    if url.find("list=") != -1:
      raise RuntimeError("This isn't a snog.")
    if url.find("https://") == -1:
      url = await self.__search(url)[0]["id"]
    a=True
    while a:
      try:
        data = await self.__datatry(pafy.new, url)
        a=False
      except:
        continue
    for property, content in vars(data).items():
      if property in self.__noNeed: continue
      self.__nowData[property.strip("_")] = content
    self.__prevData = self.__nowData
    return data

  async def songList(self, size : int, url : str):
    data = await self.__search(url)
    results = []
    if len(data) < size:
      size = len(data)
    for i in range(0, size):
      results.append(data[i])
    return results

  async def getAll(self, url : str):
    if url.find("list=") != -1:
      raise RuntimeError("This isn't a snog.")
    all = await self.__getPafy(url)
    audio = await self.__datatry(all.getbest)
    all_data = {
      "stream": audio,
      "url": {
        "vurl": self.__nowData["watchv_url"],
        "aurl": audio.url_https
      },
      "id": self.__nowData["videoid"],
    }
    all_data = {**self.__nowData, **all_data}
    del all_data["watchv_url"]
    del all_data["videoid"]
    return all_data

  async def getVideo(self, url : str):
    if url.find("list=") != -1:
      raise RuntimeError("This isn't a snog.")
    video = await self.__getPafy(url)
    video_data = {
      "stream": await self.__datatry(video.getbestvideo),
      "url": self.__nowData["watchv_url"],
      "id": video.videoid,
    }
    video_data = {**self.__nowData, **video_data}
    del video_data["watchv_url"]
    del video_data["videoid"]
    return video_data

  async def getAudio(self, url : str):
    video = await self.__getPafy(url)
    audio = await self.__datatry(video.getbestaudio)
    audio_data = {
      "stream": audio,
      "url": audio.url_https,
      "id": video.videoid,
      "title": video.title,
      "length": video.length
    }
    return audio_data

  async def __getList(self, url : str):
    return await self.__datatry(self.searchList, url)

  async def getAudioList(self, url : str, stream : bool = True):
    if url.find("list=") == -1:
      raise RuntimeError("This isn't a list")
    data_list = await self.__getList(url.split("list=")[1])
    audio_list = {}
    for i in data_list:
      Pafy = await self.getAudio(i)
      audio_list[Pafy["id"]] = Pafy
    return audio_list

  async def getVideoList(self, url : str, stream : bool = True):
    if url.find("list=") == -1:
      raise RuntimeError("This isn't a list")
    data_list = await self.__getList(url.split("list=")[1])
    video_list = {}
    for i in data_list:
      Pafy = await self.getVideo(i)
      video_list[Pafy["id"]] = Pafy
    return video_list

  async def getAllList(self, url : str, stream : bool = True):
    if url.find("list=") == -1:
      raise RuntimeError("This isn't a list")
    data_list = await self.__getList(url.split("list=")[1])
    video_list = {}
    for i in data_list:
      Pafy = await self.getAll(i)
      video_list[Pafy["id"]] = Pafy
    return video_list
  
  def download(self, stream, path : str):
    stream.download(filepath=path, quiet=True)