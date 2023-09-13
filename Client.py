import cv2
import socket
import pickle
import struct

# Client socket setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.56.1' # Replace with the server IP address
port = 8888
client_socket.connect((host_ip, port))

data = b""
payload_size = struct.calcsize("L")

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)
        if not packet:
            break
        data += packet

    if not data:
        break

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Deserialize the frame using pickle
    frame = pickle.loads(frame_data)

    # Display the received frame
    cv2.imshow('Client', frame)
    cv2.waitKey(1)

# Close the connection and destroy any open windows
cv2.destroyAllWindows()
client_socket.close()
