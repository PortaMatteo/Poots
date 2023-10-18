import socket, cv2, pickle,struct
import os
from ultralytics import YOLO
import cv2
import math
#import RPi.GPIO as GPIO
import time 
from playsound import playsound

# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 9997

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(14,GPIO.OUT)  #Il numero si riverisce al nome del pin
model_path = os.path.join('.','runs', 'detect', 'train4', 'weights', 'best.pt')
# model
model = YOLO(model_path)


# object classes
classNames = ["poop"
              ]
#cap = cv2.VideoCapture(0)
#cap.set(3, 544)
#cap.set(4, 416)


# Socket Bind
server_socket.bind((host_ip,port))

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:",host_ip,port)

conn, addr = server_socket.accept()

data = b""
payload_size = struct.calcsize("Q")

def recogntion(img):
    results = model(img, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes
        print(boxes)
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

            #cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
           
        
            return confidence >= 0.40
    return False

while True:
    while len(data) < payload_size:
        packet = conn.recv(1024) 
        if not packet: break
        data+=packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += conn.recv(1024)

    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data)
    message = str(recogntion(frame))
    conn.sendall(message.encode('utf-8'))
                

    cv2.imshow("RECEIVING VIDEO",frame)
    #message = "True"
    #conn.sendall(message.encode('utf-8'))
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'):
        break


            
server_socket.close()