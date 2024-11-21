from serial import Serial
import time

CLOSED = 0
OPEN = 180

serial = Serial('/dev/ttyUSB0', 9600)

commands = []

def read():
    line = serial.readline().decode();
    if line.startswith('#'):
        print(line, end='');
        return read()

    return line[:len(line) - 2]

def write(data):
    serial.write(bytes(data, "ascii"))
    serial.write(b"\n")

while read() != "READY":
    print("Esperando placa...")
    time.sleep(1)

while True:
    write("DISTANCE")

    d1 = int(read());
    d2 = int(read());

    if d1 < 10:
        write("LED")
        write("ON")

        write("SERVO2")
        write("VERTICAL")
        time.sleep(3)
        write("SERVO2")
        write("HORIZONTAL")
        time.sleep(1)

        write("SERVO1")
        write("VERTICAL")
        time.sleep(3)
        write("SERVO1")
        write("HORIZONTAL")

        write("LED")
        write("OFF")

    if d2 < 10:
        write("LED")
        write("ON")

        write("SERVO1")
        write("VERTICAL")
        time.sleep(3)
        write("SERVO1")
        write("HORIZONTAL")
        time.sleep(1)

        write("SERVO2")
        write("VERTICAL")
        time.sleep(3)
        write("SERVO2")
        write("HORIZONTAL")

        write("LED")
        write("OFF")

    print(d1, d2)
    time.sleep(0.5)

    
serial.close()
