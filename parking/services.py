from base64 import b64encode
from os import path
import json

from gevent import sleep

from . import image
from .plate import Plate, encode_json as plate_json_encoder

_is_started = False


def update_live_capture(socketio, capture_url, data_dir):
    global _is_started

    if _is_started:
        return
    _is_started = True

    while True:
        sleep(0.5)

        path = image.download(capture_url, data_dir, "live.jpg")
        with open(path, "rb") as file:
            encoded = b64encode(file.read())

        socketio.emit("live", encoded.decode())


def add_plate(socketio, plates, data_dir):
    plates.append(Plate(path.join(data_dir, "live.jpg")))
    socketio.emit("plates", json.dumps(plates, default=plate_json_encoder))
    print("Saved plate:", plates[-1].plate)
