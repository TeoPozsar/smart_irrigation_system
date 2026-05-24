import random
from datetime import datetime
import time
import firebase_admin
from firebase_admin import credentials, firestore
import board 
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO

# Initialize Firebase
cred = credentials.Certificate("smart-irrigation-fd7ae-firebase-adminsdk-fbsvc-adbe6d3445.json")
try:
  firebase_admin.get_app()
except ValueError:
  firebase_admin.initialize_app(cred)


db = firestore.client()

#i2c setup
i2c = busio.I2C(board.SCL, board.SDA)

#ads1115 setup
ads=ADS.ADS1115(i2c)

#read from A0
chan = AnalogIn(ads,0)


RELAY_PIN =17
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN,GPIO.OUT,initial=GPIO.HIGH)




pump_state = False
status=""


def read_moisture():
   raw_value= chan.value
   
   dry_value=20000
   wet_value=12000

   #convert sensor value tuo %
   moisture=((dry_value -raw_value) / (dry_value - wet_value)) *100

   #keep betweeen 0 and 100
   moisture= max(0,min(100,moisture))

   return int(moisture)

def control_pump(moisture):
    global pump_state
    

    if moisture < 40:
       print("pump on")
       GPIO.setup(RELAY_PIN, GPIO.OUT)
       GPIO.output(RELAY_PIN , GPIO.LOW)
       time.sleep(5)
       GPIO.output(RELAY_PIN, GPIO.HIGH)
       time.sleep(1)
       GPIO.setup(RELAY_PIN, GPIO.IN)
       print("soil watered")
          
       
    else:
        GPIO.setup(RELAY_PIN , GPIO.IN)
        print("monitoring soil")

        if pump_state:
          print("Pump off")

        pump_state = False
        


while True:
    moisture = read_moisture()

    print(f"Moisture: {moisture}%")
    control_pump(moisture)

    # send to Firebase
    db.collection("sensor_data").add({
        "moisture": moisture,
        "pump": pump_state,
        "timestamp": datetime.now(),
        "status": status
    })

    print("📡 Data sent to Firebase")

    time.sleep(5)


GPIO.cleanup()
