import socket
import ssl

SERVER_IP = "127.0.0.1"   # 👈 change this
PORT = 7000

context = ssl.create_default_context()

# since it's self-signed:
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

secure_sock = context.wrap_socket(sock, server_hostname=SERVER_IP)

secure_sock.connect((SERVER_IP, PORT))

message = "Hello Secure Server!"
secure_sock.send(message.encode())

response = secure_sock.recv(1024).decode()
print("🔒 Server says:", response)

secure_sock.close()