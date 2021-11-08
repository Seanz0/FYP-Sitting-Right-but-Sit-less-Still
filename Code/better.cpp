from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=24, trigger=25)
while True:
    print('Distance: ', sensor.distance * 100)
    sleep(1)
