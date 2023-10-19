import socket,cv2, pickle,struct, imutils
import time
#import RPi.GPIO as GPIO
from threading import Thread

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.1.13' # paste your server ip address here
port = 9997
client_socket.connect((host_ip,port))
data = b""
payload_size = struct.calcsize("Q")
vibro  = False
tstart = 0

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(14,GPIO.OUT) 


def trigger():
    print("acceso")
    #GPIO.output(14,GPIO.HIGH)
    time.sleep(5)
    #GPIO.output(14,GPIO.LOW)
    print("spento")


while True:
    if client_socket:
        cap = cv2.VideoCapture(0)

        while(cap.isOpened()):
            img,frame = cap.read()
            frame = imutils.resize(frame,width=320)
            a = pickle.dumps(frame)
            message = struct.pack("Q",len(a))+a
            client_socket.sendall(message)
            
            cv2.imshow('TRANSMITTING VIDEO',frame)
            encodedMessage = client_socket.recv(1024)
            message = encodedMessage.decode('utf-8').lower() == "true"
            print(message)
            if message:
                if vibro == False:
                    vibro = True
                    tstart = time.time()
                    #GPIO.output(14,GPIO.HIGH)
                    #playsound("success-fanfare-trumpets-6185.mp3")
                    print("ACCESOOOOACCESOOOOOOACCESOOOOOOOO")
            
            if time.time() - tstart >= 5 and vibro == True:
                #GPIO.output(14,GPIO.LOW)
                #playsound("wah-wah-sad-trombone-6347.mp3")
                vibro = False
                print("SPENTOSPENTOSPENTOSPENTOSPENTO")
            
            '''
            if message:
                if time.time() - tstart >= 5: 
                    tstart = time.time()
                    Thread(target=trigger).start()'''


            key = cv2.waitKey(1) & 0xFF
            if key ==ord('q'):
                client_socket.close()