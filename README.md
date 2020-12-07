# Pytdl Python的YTDL!

***

目前有八種功能~~

| 方法 | 傳回參數 |
| :-----: | :-----: |
| `songList(size, url)` | list |
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

## songList(size, url)

```py
a = await ydl.songList(12, "...")
print(a[0]) 
"""
{"id": ..., "title": ..., "thumbnail": ..., "length": ...}
"""
```