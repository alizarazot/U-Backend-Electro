from time import sleep
from urllib.request import urlopen

from serial import Serial

serial = Serial('/dev/ttyUSB0', 9600)

def read():
    line = serial.readline().decode();
    if line.startswith('#'):
        print(line, end='');
        return read()

    return line[:len(line) - 2]

def write(data):
    serial.write(bytes(data, "ascii"))
    serial.write(b"\n")

def url_get(url):
    r = None
    with urlopen(url) as response: r = response.read()
    return r

while read() != "READY":
    print("Esperando placa...")
    sleep(1)

while True:
    sleep(0.5)

    write("DISTANCE")

    d1 = int(read());
    d2 = int(read());

    # Sensor de la salida.
    if d1 < 10:
        write("LED")
        write("ON")

        write("SERVO2")
        write("VERTICAL")
        sleep(3)

        status =url_get("http://localhost:8000/_/car/out").decode() 

        write("SERVO2")
        write("HORIZONTAL")

        if status == "OK":
            print("Carro aceptado.")

            write("SERVO1")
            write("VERTICAL")
            sleep(3)
            write("SERVO1")
            write("HORIZONTAL")
        else:
            print("Carro rechazado.")

        write("LED")
        write("OFF")

    # Sensor de la entrada.
    if d2 < 10:
        write("LED")
        write("ON")

        write("SERVO1")
        write("VERTICAL")
        sleep(3)

        status =url_get("http://localhost:8000/_/car/in").decode() 

        write("SERVO1")
        write("HORIZONTAL")


        if status == "OK":
            print("Carro aceptado.")

            write("SERVO2")
            write("VERTICAL")
            sleep(3)
            write("SERVO2")
            write("HORIZONTAL")
        elif status == "#":
            print("Placa ya en el parqueadero.")

            write("SERVO1")
            write("VERTICAL")
            sleep(5)
            write("SERVO1")
            write("HORIZONTAL")
        else:
            print("Carro rechazado.")

        write("LED")
        write("OFF")
    
serial.close()
