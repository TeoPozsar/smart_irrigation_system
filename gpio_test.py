import RPi.GPIO as GPIO
import time

RELAY_PIN = 17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(RELAY_PIN, GPIO.OUT)

GPIO.output(RELAY_PIN, 1)

time.sleep(2)

while True:

    print("ON")
    GPIO.output(RELAY_PIN, 0)
    time.sleep(2)

    print("OFF")
    GPIO.output(RELAY_PIN, 1)
    time.sleep(2)
