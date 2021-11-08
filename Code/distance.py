import lcd
import time
import RPi.GPIO as GPIO
def distance():
    GPIO.setmode(GPIO.BOARD)
    trig=11
    echo=13
    GPIO.setup(trig,GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)
    GPIO.output(trig,GPIO.LOW)
    GPIO.output(trig,GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig, GPIO.LOW)
    while GPIO.input(echo)==0:
        Start= time.time()
    while GPIO.input(echo)==1:
        End= time.time()
    duration=End-Start
    distance=171.5*duration
    print(distance)
    return distance
distance()
GPIO.cleanup()
