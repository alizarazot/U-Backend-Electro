# Script principal.


# El modelo de concurrencia utilizado es GEvent (corutinas).
from gevent import monkey, spawn

# La librería estándar debe ser parcheada.
monkey.patch_all()

import warnings

# Eliminar advertencias molestas.
warnings.simplefilter(action="ignore", category=FutureWarning)

import os
import json
import logging

from os import path
from urllib.error import URLError

from flask import Flask, render_template, send_file
from flask_socketio import SocketIO

from . import services

# Variables de entorno.

CAPTURE_URL = os.getenv("CAPTURE_URL") or "http://192.168.0.110/capture"
CAPTURE_WAIT = 0.5
if capture_wait := os.getenv("CAPTURE_WAIT"):
    CAPTURE_WAIT = float(capture_wait)

# TODO: Usar directorio de datos general.
DATA_DIR = os.getenv("DATA_DIR") or path.abspath(
    path.join(path.dirname(__file__), "..", "parking-data")
)


# Singletons.

app = Flask(__name__)
socketio = SocketIO(app)

data_plates = []


# Página principal.
@app.route("/")
def route_home():
    spawn(lambda: services.update_live_capture(socketio, CAPTURE_URL, DATA_DIR)).join()
    spawn(lambda: services.update_plates(socketio, data_plates)).join()
    return render_template("home.html")


@app.route("/_/car/in")
def route_notify_car_in():
    socketio.emit("car-in")
    spawn(services.add_plate(socketio, data_plates, DATA_DIR)).join()
    return "Adding car..."


@app.route("/_/car/out")
def route_notify_car_out():
    socketio.emit("car-out")
    return "Removing car..."


# Eventos de Socket.IO
@socketio.on("connected")
def socket_connected(data):
    print("Connected client:", data)


if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    socketio.run(app, host="localhost", port=8000)
