import pafy
from aiohttp import ClientSession
import urllib as u
import json
from bs4 import BeautifulSoup as bs

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

  async def __fetch(self, link : str, session : ClientSession):
    async with session.get(link) as response:
      html_body = await response.text()
      return html_body

  async def __datatry(self, ex, *args):
    a=True
    while a:
      try:
        data = ex(*args)
        a=False
      except:
        continue
    return data
  
  async def __search(self, content : str):
    async with ClientSession() as session:
      response = await self.__fetch(f'https://www.youtube.com/results?search_query={u.parse.quote(content).replace("%20", "+")}', session)
    scripts = bs(response, "html.parser").find_all("script")
    for js in scripts:
      if len(str(js)) > 100000:
        script = str(js)
    obj = json.loads(script.replace(script[:script.find("var")], "").strip(";\n// scraper_data_end\n</script>").strip("var ytInitialData = "))
    content = obj["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
    if "itemSectionRenderer" in content[0]:
      data = content[0]["itemSectionRenderer"]["contents"]
    else:
      data = content[1]["itemSectionRenderer"]["contents"]
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
    return await self.__datatry(pafy.get_playlist, url)

  async def getAudioList(self, url : str):
    if url.find("list=") == -1:
      raise RuntimeError("This isn't a list")
    data_list = await self.__getList(url)
    audio_list = {}
    for Pafy in data_list["items"]:
      audio = await self.__datatry(Pafy["pafy"].getbestaudio)
      audio_list[Pafy["pafy"].videoid] = {
        "stream": audio,
        "url": audio.url_https,
        "id": Pafy["pafy"].videoid,
        "title": Pafy["pafy"].title,
        "length": Pafy["pafy"].length
      }
    return audio_list

  async def getVideoList(self, url : str):
    if url.find("list=") == -1:
      raise RuntimeError("This isn't a list")
    data_list = await self.__getList(url)
    video_list = {}
    for Pafy in data_list["items"]:
      video = await self.__datatry(Pafy["pafy"].getbestvideo)
      video_list[Pafy["pafy"].videoid] = {
        "stream": video,
        "url": Pafy["pafy"].watchv_url,
        "id": Pafy["pafy"].videoid,
        "title": Pafy["pafy"].title
      }
      await self.__getPafy(Pafy["pafy"].watchv_url)
      video_list[Pafy["pafy"].videoid] = {**video_list[Pafy["pafy"].videoid], **self.__nowData}
      del video_list[Pafy["pafy"].videoid]["watchv_url"]
      del video_list[Pafy["pafy"].videoid]["videoid"]
    return video_list
  
  def download(self, stream, path : str):
    stream.download(filepath=path, quiet=True)