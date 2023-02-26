from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import pathlib
from pathlib import Path
import config

PUBLIC_DIRECTORY = str(pathlib.Path(__file__).parent.parent) + '/' + config.web_directory

class server(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        if self.path == "/":
            data = "hello there!"
            #self.end_headers()
            #self.wfile.write(bytes(file_to_open, 'utf-8'))

            self.wfile.write(data.encode('utf-8')) 
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