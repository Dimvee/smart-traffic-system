import socket
import tkinter as tk
from collections import defaultdict
from datetime import datetime
import csv
import matplotlib.pyplot as plt

# ================= SOCKET =================
UDP_IP = "0.0.0.0"
UDP_PORT = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False)

# ================= DATA =================
node_data = defaultdict(int)

vehicle_history = []
latency_history = []
time_history = []

# 🔥 NEW: Packet loss tracking
last_seq = -1
packet_loss_count = 0
total_packets_received = 0

packet_loss_history = []
packet_index = []

key = 5

# ================= CSV =================
filename = "traffic_log.csv"
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Node", "Vehicle_Count", "Send_Time", "Receive_Time", "Seq"])

# ================= GUI =================
root = tk.Tk()
root.title("🚦 Traffic Dashboard")
root.geometry("500x400")

tk.Label(root, text="Traffic Dashboard", font=("Arial", 16, "bold")).pack(pady=10)

label_total = tk.Label(root, text="Total Vehicles: 0")
label_total.pack()

label_avg = tk.Label(root, text="Average Traffic: 0")
label_avg.pack()

label_busy = tk.Label(root, text="Busiest Signal: None")
label_busy.pack()

label_alert = tk.Label(root, text="Status: Normal", fg="green")
label_alert.pack(pady=10)

label_loss = tk.Label(root, text="Packet Loss: 0 (0%)", fg="blue")
label_loss.pack()

label_last = tk.Label(root, text="Last Update: --")
label_last.pack()

# ================= GRAPH FUNCTION =================
def show_graphs():
    if len(vehicle_history) == 0:
        print("No data")
        return

    plt.figure()
    plt.plot(time_history, vehicle_history, marker='o')
    plt.title("Traffic Flow Over Time")
    plt.xlabel("Time")
    plt.ylabel("Vehicles")
    plt.xticks(rotation=45)

    plt.figure()
    plt.plot(range(len(latency_history)), latency_history, marker='o')
    plt.title("Network Latency")
    plt.xlabel("Packet")
    plt.ylabel("Latency")

    plt.figure()
    plt.bar(range(len(vehicle_history)), vehicle_history)
    plt.axhline(y=15)
    plt.title("Congestion Detection")

    # 🔥 NEW GRAPH
    plt.figure()
    plt.plot(packet_index, packet_loss_history, marker='o')
    plt.title("Packet Loss Over Time")
    plt.xlabel("Sequence Number")
    plt.ylabel("Total Packets Lost")

    plt.tight_layout()
    plt.show()

tk.Button(root, text="📊 Show Graphs", command=show_graphs).pack(pady=10)

# ================= UPDATE =================
def update_data():
    global last_seq, packet_loss_count, total_packets_received

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            message = data.decode()

            print("Received:", message)

            node, vehicle, send_time, seq_num = message.split(",")

            vehicle = int(vehicle) - key
            seq_num = int(seq_num)

            total_packets_received += 1

            # 🔥 PACKET LOSS DETECTION
            if last_seq != -1:
                expected = last_seq + 1
                if seq_num > expected:
                    loss = seq_num - expected
                    packet_loss_count += loss
                    print(f"⚠️ Packet Loss Detected: {loss}")

            last_seq = seq_num

            packet_loss_history.append(packet_loss_count)
            packet_index.append(seq_num)

            receive_time = datetime.now().strftime("%H:%M:%S")

            node_data[node] = vehicle

            vehicle_history.append(vehicle)
            time_history.append(send_time)

            latency = (datetime.now() - datetime.strptime(send_time, "%H:%M:%S")).total_seconds()
            latency_history.append(latency)

            # 🔥 Packet loss %
            total_sent_estimate = packet_loss_count + total_packets_received
            loss_percent = (packet_loss_count / total_sent_estimate) * 100 if total_sent_estimate > 0 else 0

            label_loss.config(text=f"Packet Loss: {packet_loss_count} ({loss_percent:.2f}%)")

            with open(filename, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([node, vehicle, send_time, receive_time, seq_num])

            total = sum(node_data.values())
            avg = total / len(node_data)
            busiest = max(node_data, key=node_data.get)

            label_total.config(text=f"Total Vehicles: {total}")
            label_avg.config(text=f"Average Traffic: {avg:.2f}")
            label_busy.config(text=f"Busiest Signal: {busiest}")
            label_last.config(text=f"Last Update: {receive_time}")

            if vehicle > 15:
                label_alert.config(text=f"🚨 Congestion at {node}", fg="red")
            else:
                label_alert.config(text="Status: Normal", fg="green")

    except BlockingIOError:
        pass
    except Exception as e:
        print("Error:", e)

    root.after(500, update_data)

update_data()
root.mainloop()