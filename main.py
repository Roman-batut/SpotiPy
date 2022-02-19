#Imports
import csv 
from youtubesearchpython import VideosSearch
import youtube_dl
from ShazamAPI import Shazam
import asyncio

#Open CSV
fields = []
titles = []

with open("playlist.csv", "r", encoding = "utf8") as f :
    file = csv.reader(f, delimiter = ',')
    
    fields = next(file)

    for row in file :
        titles.append(row[0])


#Functions youtube
def ytMusicAPI(name) :
    search_link = VideosSearch(str(name), limit = 1)
    video_url = search_link.result()["result"][0]["link"]
    
    return(video_url)

def ytMusicDownload(name, url) :
    ydl_opts = {
        'outtmpl': "music/" + str(name).replace(" ","_") + ".mp3",
        'format':
            'bestaudio/best',
            'postprocessors': 
                [{  
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320', 
                    }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as Mp3 :
        Mp3.download([url])

#Function shazam
async def shazam(title) :
    music = "music/" + str(title.replace(" ", "_")) + ".mp3"
    mp3 = open(music, 'rb').read()

    shazam = Shazam(mp3)
    recognize_generator = shazam.recognizeSong()

    return(next(recognize_generator))

#Search youtube urls and download
urls = []
shazamed = []
loop = asyncio.get_event_loop()

for title in titles :
    url = ytMusicAPI(title)
    try :
        ytMusicDownload(title, url)
    except : pass
    musique = loop.run_until_complete(shazam(title))
    shazamed.append(musique)
    urls.append(url)
   
