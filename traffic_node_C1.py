import socket
import time
import random
from datetime import datetime

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

node_name = "Signal_A"
key = 5   # 🔐 encryption key

seq_num = 0   # 🔥 NEW: sequence number

print("🚗 Client started...\n")

while True:
    vehicle_count = random.randint(5, 25)

    # 🔐 Encrypt
    encrypted_vehicle = vehicle_count + key

    current_time = datetime.now().strftime("%H:%M:%S")

    # 🔥 Simulate packet loss (20%)
    if random.random() < 0.2:
        print("⚠️ Packet DROPPED (simulated)")
        seq_num += 1
        time.sleep(2)
        continue

    seq_num += 1

    message = f"{node_name},{encrypted_vehicle},{current_time},{seq_num}"

    sock.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

    print(f"Sent (encrypted): {message}")

    time.sleep(2)