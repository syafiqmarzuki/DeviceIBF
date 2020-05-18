import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library


GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 
GPIO.setwarnings(False)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)

def ping(echo, trig):
    
    GPIO.output(trig, False)
    # Allow module to settle
    time.sleep(0.5)
    # Send 10us pulse to trigger
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
    pulse_start = time.time()

    # save StartTime
    while GPIO.input(echo) == 0:
        pulse_start = time.time()

    # save time of arrival
    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    # time difference between start and arrival
    pulse_duration = pulse_end - pulse_start
    # mutiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = pulse_duration * 17150
    
    distance = round(distance, 2)
    
    return distance





