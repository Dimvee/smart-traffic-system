Smart Traffic Management System
Computer Networks Project
README & Project Documentation

1. Project Overview
This project simulates a Smart Traffic Management System using UDP socket communication, Caesar cipher encryption, congestion detection, and real-time GUI analytics. Multiple traffic signal nodes (clients) send encrypted vehicle count data to a central server, which decrypts and forwards data to a GUI-based analysis dashboard.

2. Key Features
•	UDP-based real-time communication between traffic nodes and server
•	Caesar cipher encryption of vehicle count data (key = 5)
•	Simulated packet loss (~20% drop rate) with sequence number tracking
•	Congestion detection when vehicle count exceeds 15 vehicles
•	Real-time Tkinter GUI dashboard displaying traffic statistics
•	Matplotlib graphs: Traffic Flow, Network Latency, Congestion Detection, Packet Loss
•	CSV logging of all traffic data to traffic_log.csv
•	SSL/TLS support via ssl_server.py and ssl_client.py

3. Project File Structure
The project contains the following files:

File	Description
traffic_server.py	UDP server that receives encrypted data, decrypts it, detects congestion, and forwards to analysis GUI
traffic_node_C1.py	Traffic client for Signal_A — generates random vehicle counts, encrypts, and sends via UDP
traffic_node_C2.py	Traffic client for Signal_B — same as C1 but reports Signal_B data
traffic_node_C3.py	Traffic client for Signal_C — third signal node
analysis_gui.py	Tkinter GUI dashboard — receives data, shows stats, detects congestion, logs CSV, displays graphs
ssl_server.py	TLS/SSL-secured version of the traffic server
ssl_client.py	TLS/SSL-secured version of the traffic client
server.crt	SSL certificate file for secure communication
server.key	SSL private key file
traffic_log.csv	Auto-generated CSV log of all traffic data (Node, Count, Send Time, Receive Time, Seq)

4. System Architecture
The system follows a client-server architecture over UDP:

Traffic Nodes (C1, C2, C3)  →  [UDP Port 5005]  →  Traffic Server  →  [UDP Port 6000]  →  Analysis GUI

Each traffic node independently generates random vehicle counts every 2 seconds, applies Caesar cipher encryption (adds 5 to the vehicle count), and sends the encrypted message to the server. The server decrypts, checks for congestion, and forwards all data to the GUI on port 6000. The GUI tracks sequence numbers to detect packet loss.

5. How to Run
Prerequisites
•	Python 3.x installed
•	Required libraries: socket, tkinter, matplotlib, csv, datetime (all standard library)

Step-by-Step Instructions
Step 1 — Start the Analysis GUI (must be first):
python analysis_gui.py
Step 2 — Start the Traffic Server:
python traffic_server.py
Step 3 — Start one or more Traffic Nodes (in separate terminals):
python traffic_node_C1.py
python traffic_node_C2.py
python traffic_node_C3.py
Step 4 — In the GUI dashboard, click Show Graphs to view the analytics.

6. Technical Details
Network Protocol
•	Transport Layer: UDP (User Datagram Protocol)
•	Server listens on port 5005 for node data
•	GUI listens on port 6000 for forwarded server data
•	All communication is on localhost (127.0.0.1)

Encryption
•	Algorithm: Caesar cipher (shift cipher)
•	Key: 5 (added on encrypt, subtracted on decrypt)
•	Applied to vehicle count integer values only

Message Format
Each packet sent has the following comma-separated format:
NodeName,EncryptedVehicleCount,HH:MM:SS,SequenceNumber
Example: Signal_A,28,12:01:05,4  (28 encrypted = 23 actual vehicles)

Congestion Threshold
•	Congestion is flagged when decrypted vehicle count > 15
•	Server prints 'CONGESTION DETECTED!' and GUI shows red alert

Packet Loss Simulation
•	Each node randomly drops ~20% of packets before sending
•	Sequence numbers allow the GUI to detect and count lost packets
•	Packet loss % is displayed live in the dashboard

7. Screenshots
The following screenshots demonstrate the system running in action.

7.1 Client Nodes Terminal
Both Signal_A (C1) and Signal_B (C2) clients running simultaneously, showing encrypted packets sent and simulated dropped packets.
 
Figure 1 — Client Nodes C1 (Signal_A) and C2 (Signal_B) terminal output
7.2 Server Terminal
The traffic server decrypting incoming packets, printing vehicle counts per signal, and detecting congestion events.
 
Figure 2 — Traffic Server terminal showing decrypted data and congestion alerts
7.3 Traffic Dashboard GUI
The real-time Tkinter dashboard showing total vehicles, average traffic, busiest signal, congestion alert, and packet loss statistics.
 
Figure 3 — Traffic Dashboard GUI showing live statistics and congestion alert at Signal_B
7.4 Traffic Flow Over Time
Line graph plotting vehicle counts over real-time timestamps, showing traffic density fluctuations across the monitoring period.
 
Figure 4 — Traffic Flow Over Time graph (vehicles vs. timestamp)
7.5 Network Latency
Graph showing the one-way latency (in seconds) for each received packet, calculated as the difference between send time and receive time.
 
Figure 5 — Network Latency per packet (y-axis offset: +3.9853728e9)
7.6 Congestion Detection
Bar chart of vehicle counts per packet. The horizontal threshold line at 15 vehicles marks the congestion boundary. Bars above the line represent congestion events.
 
Figure 6 — Congestion Detection bar chart with threshold at 15 vehicles
7.7 Packet Loss Over Time
Scatter/line plot of cumulative packet loss count against sequence numbers, demonstrating the effect of the 20% simulated drop rate over time.
 
Figure 7 — Cumulative Packet Loss Over Time

8. Notes & Limitations
•	The system uses UDP which is connectionless — no guarantee of delivery (intentional for simulation).
•	Packet loss is simulated in the client nodes, not caused by actual network failure.
•	Latency values may appear large due to datetime parsing across midnight boundaries.
•	For secure communication, use ssl_server.py and ssl_client.py with the provided certificate files.
•	The CSV log (traffic_log.csv) is overwritten each time analysis_gui.py starts.

Smart Traffic Management System — Computer Networks Project
