import RPi.GPIO as GPIO
import time

RELAY_PIN =17

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

print("LOW")
GPIO.output(RELAY_PIN, GPIO.LOW)
time.sleep(5)

print("HIGH")
GPIO.output(RELAY_PIN, GPIO.HIGH)
time.sleep(5)

GPIO.cleanup()
