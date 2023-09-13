import cv2
import socket
import pickle
import struct

# Server socket setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = '192.168.56.1' # Enter Your IP Address
print('HOST IP:', host_ip)
port = 8888
socket_address = (host_ip, port)

server_socket.bind(socket_address)
server_socket.listen(5)
print("Waiting for a connection...")
client_socket, client_addr = server_socket.accept()
print("CONNECTED!")

# Open the camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Serialize the frame using pickle
    data = pickle.dumps(frame)

    # Pack the serialized data and send it to the client
    message_size = struct.pack("L", len(data))
    client_socket.sendall(message_size + data)

    # Display the frame (optional)
    cv2.imshow('Server', frame)
    cv2.waitKey(1)

# Release the camera and close the connection

cap.release()
cv2.destroyAllWindows()
client_socket.close()
server_socket.close()
