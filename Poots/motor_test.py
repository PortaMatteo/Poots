from gpiozero import Buzzer
import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BCM)
GPIO.setup(14,GPIO.OUT)  #Il numero si riverisce al nome del pin

while True: 
    GPIO.output(14,GPIO.HIGH)
    print('acceso')


    