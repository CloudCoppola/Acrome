from smd.red import *
import time

port = "COM6" # Check COM in device manager
device_id = 0
m = Master(port)
m.attach(Red(device_id))

print(m.scan_modules(0))

while True:
    imu = m.get_imu(device_id, 5)
    print(imu)
    time.sleep(0.5)