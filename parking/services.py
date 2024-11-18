from base64 import b64encode
from os import path
import json

from gevent import sleep

from . import image
from .plate import Plate, encode_json as plate_json_encoder

_is_update_live_capture_started = False


def update_live_capture(socketio, poll_time, capture_url, data_dir):
    global _is_update_live_capture_started

    if _is_update_live_capture_started:
        return
    _is_update_live_capture_started = True

    while True:
        sleep(poll_time)

        path = image.download(capture_url, data_dir, "live.jpg")
        with open(path, "rb") as file:
            encoded = b64encode(file.read())

        socketio.emit("live", encoded.decode())


_is_update_plates_started = False


def update_plates(socketio, active_plates, inactive_plates):
    global _is_update_plates_started

    if _is_update_plates_started:
        return
    _is_update_plates_started = True

    while True:
        sleep(1)
        socketio.emit(
            "plates",
            json.dumps(
                {"active": active_plates, "inactive": inactive_plates},
                default=plate_json_encoder,
            ),
        )
