from os import path
import yt_dlp
from yt_dlp.utils import DownloadError
import config
import json

ytdl = yt_dlp.YoutubeDL()


def download(url: str) -> str:
    ydl_optssx = {
        'restrict_filenames': True,
        "outtmpl": config.web_directory + '/' + config.yt2mp3_directory + "/%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,

        #"write-thumbnail": True,
        #"write-info-json": True,
        
        'extract-audio':True,
        'audio-format':'mp3',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128'
        }]
    }
    info = ytdl.extract_info(url, False)
    try:
        x = yt_dlp.YoutubeDL(ydl_optssx)
        #x.add_progress_hook(my_hook)
        dloader = x.download([url])
    except Exception as y_e:
        return print(y_e)
    else:
        dloader
    xyz = config.web_directory + '/' + config.yt2mp3_directory + '/' + info['id'] + '.mp3'

    videoinfo = {}
    videoinfo['id'] = info['id']
    videoinfo['title'] = info['title']
    videoinfo['thumbnail'] = info['thumbnail']
    videoinfo['upload_date'] = info['upload_date']
    videoinfo['uploader'] = info['uploader']
    videoinfo['view_count'] = info['view_count']
    videoinfo['like_count'] = info['like_count']

    jsonfile = config.web_directory + '/' + config.yt2mp3_directory + '/' + videoinfo['id'] + '.json'
    with open(jsonfile, 'w') as f:
        json.dump(videoinfo, f)

    return xyz, info['title'], info['id']