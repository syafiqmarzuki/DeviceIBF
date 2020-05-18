import RPi.GPIO as GPIO
import time

def setup():
    GPIO.setmode(GPIO.BCM)
    #GPIO.setmode(GPIO.BOARD)
    GPIO.setup(4,GPIO.OUT)
    global servo
    servo=GPIO.PWM(4,50)
    servo.start(5)
        #start pwm with Duty Cycle is 2% --> Pluse with = 2%*20ms = 0.4ms
#Create PWM on pin 11 with frequency 50Hz --> period 20ms
def ServoUp():
    servo.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    
    
def ServoDown():
    servo.ChangeDutyCycle(2.5)
    time.sleep(0.5)
    
def close():
    servo.stop()
if __name__ == '__main__':
    setup()