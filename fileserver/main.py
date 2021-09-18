from utils.server import get_server


def main():
    http_server = get_server()
    http_server.serve_forever()


if __name__ == "__main__":
    main()
