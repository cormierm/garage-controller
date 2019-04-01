import RPi.GPIO as GPIO
import time
from flask import Flask, request

app = Flask(__name__)

door1 = 18
channels = [door1]

GPIO.setmode(GPIO.BCM)
GPIO.setup(channels, GPIO.OUT)

@app.route("/")
def home():
    return "Garage Door Application"

@app.route("/toggle-door")
def toggleDoor():
    try:
        channel = int(request.args.get('channel'))
    except:
        return 'Channel must be an integer'

    if channel in channels:
        triggerGPIO(channel)
        return 'Toggled {}'.format(channel)
    return "Invalid Channel"

def triggerGPIO(gpioChannel):
    GPIO.output(gpioChannel, False)
    time.sleep(1)
    GPIO.output(gpioChannel, True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')