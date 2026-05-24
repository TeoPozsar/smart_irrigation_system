import RPi.GPIO as GPIO
import time

pins = [17, 18, 27, 22, 23, 24]

GPIO.setmode(GPIO.BCM)

for pin in pins:

    print(f"Testing GPIO {pin}")

    GPIO.setup(pin, GPIO.OUT)

    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1)

    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)

GPIO.cleanup()
