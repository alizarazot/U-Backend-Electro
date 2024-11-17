from base64 import b64encode

from gevent import sleep

from . import image

_is_started = False


def update_live_capture(socketio, capture_url, plates_dir):
    global _is_started

    if _is_started:
        return
    _is_started = True

    while True:
        sleep(0.5)

        path = image.download(capture_url, plates_dir, "live.jpg")
        with open(path, "rb") as file:
            encoded = b64encode(file.read())

        socketio.emit("live", encoded.decode())
