import socket
import ssl

HOST = "0.0.0.0"
PORT = 7000

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

print("🔐 SSL Server running on port 7000...\n")

while True:
    client_socket, addr = sock.accept()
    print(f"Connection from {addr}")

    try:
        secure_socket = context.wrap_socket(client_socket, server_side=True)

        data = secure_socket.recv(1024).decode()
        print(f"🔒 Received (secure): {data}")

        response = "Secure data received!"
        secure_socket.send(response.encode())

        secure_socket.close()

    except Exception as e:
        print("SSL Error:", e)