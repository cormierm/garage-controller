import RPi.GPIO as GPIO
import time
from flask import Flask, request, send_file
from picamera import PiCamera

app = Flask(__name__)

door1 = 18
channels = [door1]

GPIO.setmode(GPIO.BCM)
GPIO.setup(channels, GPIO.OUT)

@app.route("/")
def home():
    return "Garage Door Application"

@app.route("/show")
def show():
    image = open('image.jpg', 'wb')
    camera = PiCamera()
    camera.start_preview()
    time.sleep(2)
    camera.capture(image)
    return send_file(image)

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