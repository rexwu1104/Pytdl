# Pytdl Python的YTDL!

***

目前簡化為四種功能~~

| 方法 | 傳回參數 |
| :-----: | :-----: |
| `songList(query : str, size : int = 12)` | List[dict] |
| `searchList(list_id : str)` | List[str] |
| `songs(querys : List[str])` | List[songList] |
| `info(url : str)` | Song or SongList |

songList 回傳的結構為
```py
[{
	"id": str,
	"title": str,
	"thumbnail": list,
	"length": str
}, ...]
```

searchList 回傳的結構為
```py
[str, ...]
```

songs 回傳的結構為
```py
[songList(), ...]
```

info 回傳的結構為
```py
[Song() | SongList(), ...]
```

Song 與 SongList 要使用 create 創建其結構 (async func)

SongList 創建後的 SongList.songs 為一個 list

```py
from NPytdl import Pytdl
ydl = Pytdl()

song = ydl.info("https://youtu.be/RGtSdbjxVKU")

import asyncio
asyncio.run(song.create())

song.download(f"./test/{song.title}")
```

這樣就能下載這首歌
