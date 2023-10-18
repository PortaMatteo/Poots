# lets make the client code
import socket,cv2, pickle,struct, imutils

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.44.41' # paste your server ip address here
port = 9995
client_socket.connect((host_ip,port))
data = b""
payload_size = struct.calcsize("Q")
while True:
	if client_socket:
		vid = cv2.VideoCapture(0)
		
		while(vid.isOpened()):
			img,frame = vid.read()
			frame = imutils.resize(frame,width=320)
			a = pickle.dumps(frame)
			message = struct.pack("Q",len(a))+a
			client_socket.sendall(message)
			
			cv2.imshow('TRANSMITTING VIDEO',frame)
			key = cv2.waitKey(1) & 0xFF
			if key ==ord('q'):
				client_socket.close()
	
	
	
