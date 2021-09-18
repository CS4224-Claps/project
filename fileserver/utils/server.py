import http.server
import socketserver

from utils.cli import parse_cmdline

opt = parse_cmdline()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=opt.directory, **kwargs)


def get_server():
    return socketserver.TCPServer(("localhost", opt.port), Handler)
