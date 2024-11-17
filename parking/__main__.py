from gevent import monkey, sleep, spawn

monkey.patch_all()

import os
import json
import logging

from os import path
from urllib.error import URLError
from base64 import b64encode

from flask import Flask, render_template, send_file
from flask_socketio import SocketIO

from . import image
from . import plate

# Variables de entorno.
CAPTURE_URL = os.getenv("CAPTURE_URL") or "http://192.168.0.110/capture"
# TODO: Usar directorio de datos general.
PLATES_DIR = os.getenv("PLATES_DIR") or path.abspath(
    path.join(path.dirname(__file__), "data", "plates")
)


app = Flask(__name__)
socketio = SocketIO(app)

plates = []


# Página principal.
@app.route("/")
def home():
    glet = spawn(update_image)
    glet.join()
    return render_template("home.html")


is_started = False


def update_image():
    global is_started
    if is_started:
        return
    is_started = True
    while True:
        sleep(0.5)
        path = image.save_image(CAPTURE_URL, PLATES_DIR, "live.jpg")
        with open(path, "rb") as file:
            encoded = b64encode(file.read())
        socketio.emit("live", encoded.decode())


# Punto de entrada para reconocimiento de placa.
@app.route("/plate")
def plate_endpoint():
    p = plate.scan(image.save_image(CAPTURE_URL, PLATES_DIR))
    plates.append(p)
    socketio.emit("plates", json.dumps(plates))
    return p


@socketio.on("connected")
def socket_connected(data):
    print("Connected client:", data)


if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    socketio.run(app, host="localhost", port=8000)
