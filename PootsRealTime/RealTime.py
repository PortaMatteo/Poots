import os
from ultralytics import YOLO
import cv2
import math
#import RPi.GPIO as GPIO
import time 
from playsound import playsound
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(14,GPIO.OUT)  #Il numero si riverisce al nome del pin
vibro  = False
model_path = os.path.join('.','runs', 'detect', 'train', 'weights', 'best.pt')
# model
model = YOLO(model_path)
tstart = 0

# object classes
classNames = ["poop"
              ]

# start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 544)
cap.set(4, 416)

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:

            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values
            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)


            confidence = math.ceil((box.conf[0]*100))/100
            #print("Confidence --->",confidence)


            # class name
            cls = int(box.cls[0])
            #print("Class name -->", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
           
            

            if confidence >= 0.40:
                if vibro == False:
                    vibro = True
                    tstart = time.time()
                    #GPIO.output(14,GPIO.HIGH)
                    playsound("success-fanfare-trumpets-6185.mp3")
                    print("ACCESOOOOACCESOOOOOOACCESOOOOOOOO")
            if time.time() - tstart >= 5 and vibro == True:
                #GPIO.output(14,GPIO.LOW)
                playsound("wah-wah-sad-trombone-6347.mp3")
                vibro = False
                print("SPENTOSPENTOSPENTOSPENTOSPENTO")

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
