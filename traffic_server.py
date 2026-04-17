import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))

ANALYSIS_IP = "127.0.0.1"
ANALYSIS_PORT = 6000

analysis_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

key = 5

print("🚦 Server running...\n")

while True:
    data, addr = sock.recvfrom(1024)
    message = data.decode()

    try:
        node, encrypted_vehicle, send_time, seq_num = message.split(",")

        # 🔐 Decrypt
        vehicle = int(encrypted_vehicle) - key

        print(f"📡 {node} → {vehicle} vehicles | Seq: {seq_num}")

        # 🚨 Congestion check
        if vehicle > 15:
            print("🚨 CONGESTION DETECTED!\n")
        else:
            print("✅ Traffic Normal\n")

        # Forward unchanged
        analysis_sock.sendto(message.encode(), (ANALYSIS_IP, ANALYSIS_PORT))

    except Exception as e:
        print("❌ Error:", e)