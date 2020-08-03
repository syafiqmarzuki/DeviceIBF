import RPi.GPIO as GPIO
import time

servoPIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 4 for PWM with 50Hz
p.start(5) # Initialization
try:
    p.ChangeDutyCycle(7.5)
    time.sleep(0.5)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()