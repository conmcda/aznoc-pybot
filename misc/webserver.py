from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import pathlib
from pathlib import Path
import config
import json


PUBLIC_DIRECTORY = str(pathlib.Path(__file__).parent.parent) + '/' + config.web_directory

class server(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        if self.path == "/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'hi there :)')

            #self.end_headers()
            #self.wfile.write(bytes(file_to_open, 'utf-8'))

        elif self.path == "/mp3s/":
            self.send_response(200)
            self.end_headers()

            html = "<!DOCTYPE html><html><head><title>pybot - MP3 Files</title><link rel='stylesheet' href='/%s/global.css'><link rel='preconnect' href='https://fonts.googleapis.com'><link rel='preconnect' href='https://fonts.gstatic.com' crossorigin><link href='https://fonts.googleapis.com/css2?family=Noto+Sans:wght@100;300;400;700&display=swap' rel='stylesheet'></head><body><div id='topbar'><div id='logo'>pybot</div></div><div id='main'><div id='mp3s'><ul>" % (config.web_res_directory)

            files = os.listdir(PUBLIC_DIRECTORY+self.path)

            for file in files:
                if (file.endswith('mp3')):
                    vid = file[:-4]
                    jsonfilepath = PUBLIC_DIRECTORY+self.path + '/%s.json' % vid

                    with open(jsonfilepath) as jsonfile:
                        vidinfo = json.load(jsonfile)
                        print('vid thumbnail = %s' % vidinfo['thumbnail'])

                    config.web_res_directory

                    html += "<li><div class='thumbnail'><img src='%s' width='64' height='64'></div><a href=''>%s</a><audio controls><source src='%s' type='audio/mpeg'>Your browser does not support the audio element.</audio><div class='dl'><a title='Download file' download='%s' href='%s'></a></div></li>" % (vidinfo['thumbnail'], vidinfo['title'], str(file), str(file), str(file))

            html += "</ul></div></div><div id='footer'>Made with love by <a href='https://github.com/azn0c' target='_blank'>aznoc</a></div></body></html>"

            self.wfile.write(str(html).encode())

        elif self.path == '/up':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Going up')

        elif os.path.isdir(PUBLIC_DIRECTORY+self.path):
            try:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(str(os.listdir(PUBLIC_DIRECTORY+self.path)).encode())
            except Exception:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'error')
        else:
            try:
                with open(PUBLIC_DIRECTORY+self.path, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(data)
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'not found')
            except PermissionError:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b'no permission')
            except Exception as e:
                print(e)
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'error')