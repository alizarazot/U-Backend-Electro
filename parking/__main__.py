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
from datetime import datetime

from flask import Flask, render_template, send_file
from flask_socketio import SocketIO

from . import services
from .plate import Plate

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

data_active_plates = []
data_inactive_plates = []


# Página principal.
@app.route("/")
def route_home():
    spawn(
        lambda: services.update_live_capture(
            socketio, CAPTURE_WAIT, CAPTURE_URL, DATA_DIR
        )
    ).join()
    spawn(
        lambda: services.update_plates(
            socketio, data_active_plates, data_inactive_plates
        )
    ).join()
    return render_template("home.html")


@app.route("/pdf/<pdf>")
def route_pdf(pdf):
    return send_file(path.join(DATA_DIR, "pdf", path.basename(pdf)))


@app.route("/_/car/in")
def route_notify_car_in():
    socketio.emit("car-in-start", ignore_queue=True)
    socketio.sleep(0)

    plate = Plate(path.join(DATA_DIR, "live.jpg"))
    if plate.plate.strip() == "":
        socketio.emit("car-in-end", None)
        return "Text not found!"
    
    data_active_plates.append(plate)
    socketio.emit("car-in-end", data_active_plates[-1].plate)

    return "Added: " + data_active_plates[-1].plate


@app.route("/_/car/out")
def route_notify_car_out():
    socketio.emit("car-out-start", ignore_queue=True)
    socketio.sleep(0)

    target = Plate(path.join(DATA_DIR, "live.jpg")).plate
    for i, plate in enumerate(data_active_plates):
        if plate.plate == target:
            data_active_plates.pop(i)
            plate.end_parking()

            elapsed_time = plate.time_out - plate.time_in
            formatted_elapsed = f"{elapsed_time.seconds // 3600} horas, {(elapsed_time.seconds % 3600) // 60} minutos, {elapsed_time.seconds % 60} segundos"

            plate.render_pdf(
                render_template(
                    "pdf.html",
                    plate=plate.plate,
                    date=datetime.now().strftime("%Y/%m/%d"),
                    time_in=plate.time_in.strftime("%I:%M %p"),
                    time_out=plate.time_out.strftime("%I:%M %p"),
                    total_time=formatted_elapsed,
                    total_price=plate.get_price(),
                    cost_hour=plate.COST_HOUR,
                ),
                DATA_DIR,
            )
            data_inactive_plates.append(plate)
            break

    socketio.emit("car-out-end", target)

    return "Removed: " + target


# Eventos de Socket.IO
@socketio.on("connected")
def socket_connected(data):
    print("Connected client:", data)


if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    socketio.run(app, host="localhost", port=8000)
