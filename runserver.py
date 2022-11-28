from os import environ
from site_example import app

if __name__ == '__main__':
    HOST = environ.get("SERVER_HOST","localhost")
    try:
        PORT = int(environ.get("SERVER_HOST","localhost"))
    except ValueError:
        PORT = 5000
    app.run(HOST,PORT)