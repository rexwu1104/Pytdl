# Pytdl Python的YTDL!

***

目前有九種功能~~

| 方法 | 傳回參數 |
| :-----: | :-----: |
| `songList(size, url)` | List[dict] |
| `searchList(list_id)` | List[str] |
| `getAll(url)` | dict |
| `getVideo(url)` | dict |
| `getAudio(url)` | dict |
| `getAllList(list_url)` | dict |
| `getVideoList(list_url)` | dict |
| `getAudioList(list_url)` | dict |
| `download(stream, path)` | none |

Video 和 All 的相關功能會回傳影片資訊
Audio 則不會
Video/Audio 皆有的屬性有:

- **stream**
- **url**
- **title**
- **id**

List 的相關功能是以個別影片的 ID 為 Key, 可以用以下方法獲得

```py
for id in List:
  print(List[id])
```

```py
from NPytdl import Pytdl
ydl = Pytdl()

song = ydl.getAudio("https://youtu.be/RGtSdbjxVKU")

ydl.download(song["stream"], f"./test/{song['title']}")
```

這樣就能下載這首歌
