from NPytdl import (
	Pytdl,
	SpotifyMusics,
	SpotifyMusic,
	YoutubeVideos,
	YoutubeVideo
)
from NPytdl.webBug import get, spotifyGet
from NPytdl.dataParser import Parser
import asyncio
import os


ydl = Pytdl()
loop = asyncio.get_event_loop()
l = YoutubeVideo('https://www.youtube.com/watch?v=40dJS_LC6S8')

a = loop.run_until_complete(
	l.create()
)
# print(l.videoList)

# print("歡迎使用Pytdl。")

# while True:
#   print("請問你要下載什麼歌曲呢?")
#   print("請輸入網址或是你想搜尋的影片名稱。")
#   name = input()
#   os.system("clear")
#   if name.find("https://") == -1:
#     print("看來這不是個網址呢")
#     print("沒關係，我幫你搜尋")
#     songs = loop.run_until_complete(ydl.songList(name))
#     for i in range(1, len(songs)+1):
#       print(str(i)+".", songs[i-1]["title"])
#     print("請問是哪一首呢 (請輸入數字)")
#     num=int(input())
#     while num > len(songs) or num < 1:
#       os.system("clear")
#       print("不好意思，這不再範圍內呢")
#       print("請問是哪一首呢 (請輸入數字)")
#       num=int(input())
#     os.system("clear")
#     name = "https://youtu.be/" + songs[num-1]["id"]
#   else:
#     print("好的，幫你搜尋")
#   print("那你要什麼類型?")
#   print("有 audio, video 和 normal")
#   t=input()
#   os.system("clear")
#   while t not in ["audio", "video", "normal"]:
#     print("沒有這個類型耶")
#     print("我們有 audio, video 和 normal")
#     t=input()
#   if name.find("list=") != -1:
#     if t == "audio":
#       songs = loop.run_until_complete(ydl.info(name))
#       for i in songs:
#         songs[i].stream.download(f'./test/{songs[i].title}.mp3')
#     elif t == "video":
#       pass
#     elif t == "normal":
#       pass
#   else:
#     if t == "audio":
#       print("OK. 幫你下載音訊")
#       audio = loop.run_until_complete(ydl.info(name))
#       loop.run_until_complete(audio.create())
#       audio.stream.download(f'{audio.title}.mp3')
#       if os.path.isfile(f'{audio.title}.mp3') == True:
#         print("下載完成")
#       else:
#         print("下載失敗")
#     elif t == "video":
#       print("OK. 幫你下載影片")
#       audio = loop.run_until_complete(ydl.info(name))
#       loop.run_until_complete(audio.create())
#       audio.stream.download(f'{audio.title}.mp4', "video")
#       if os.path.isfile(f'{audio.title}.mp4') == True:
#         print("下載完成")
#       else:
#         print("下載失敗")
#   print("請問你還要下載嗎? (Y/N)")
#   ans=input()
#   if ans == "N" or ans == "n":
#     break
#   os.system("clear")