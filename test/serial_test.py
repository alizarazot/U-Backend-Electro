from serial import Serial
import time

CLOSED = 0
OPEN = 180

serial = Serial('COM4', 9600)

while True:
    line = serial.readline().decode();
    print(line)
    if line.startswith('#'): continue
    
    sensor, distance = line.split(' ')
    distance = distance[:len(distance)-2]
    #print(sensor, distance+"cm")
    if sensor == "DISTANCE1": continue
    
    print("--Writting")
    serial.write(f'{CLOSED}\n'.encode())
    while True:
        line = serial.readline().decode();
        print(line)
        if line.startswith("OK"): break
    time.sleep(1)
    serial.write(f'{OPEN}\n'.encode())
    print("-- Ending")
    time.sleep(2)
    
    
serial.close()