from os import path
import yt_dlp
from yt_dlp.utils import DownloadError
import config

ytdl = yt_dlp.YoutubeDL()


def download(url: str) -> str:
    ydl_optssx = {
        'restrict_filenames': True,
        "outtmpl": config.web_directory + '/' + config.yt2mp3_directory + "/%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
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
    return xyz, info['title'], info['id']