# Pytdl (NPytdl)

***

We have nine methods for `Pytdl` class

| method | return |
| :-----: | :-----: |
| `resultList(query : str)` | json |
| `spotifyResultList(query : str)` | json |
| `playList(list_id : str)` | json |
| `spotifyPlayList(list_id : str)` | json |
| `resultsList(querys : List[str])` | json |
| `spotifyResultsList(querys : List[str])` | json |
| `next(id : str)` | json |
| `spotifyTrack(id : str)` | json |
| `info(url : str)` | YoutubeVideos \| YoutubeVideo \| SpotifyMusics \| SpotifyMusic |

```py
from NPytdl import Pytdl
ydl = Pytdl()

song = ydl.info("https://youtu.be/RGtSdbjxVKU")

import asyncio
asyncio.run(song.create())

song.download(f"./test/{song.title}")
```
