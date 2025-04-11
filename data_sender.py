import socket
import time

# Define target IP & port
TARGET_IP = "192.168.2.2"  # Change to your target device's IP
TARGET_PORT = 5005

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define packet size (in bytes)
PACKET_SIZE = 7500 // 8  # 7500 bits = 937 bytes
PACKET = b'X' * PACKET_SIZE  # Sample data

# Define transmission rate (packets per second)
PACKETS_PER_SECOND = 60_000 // (PACKET_SIZE * 8)  # Adjust for 60k bps

print(f"Sending data to {TARGET_IP}:{TARGET_PORT} at 60k bps...")

while True:
    start_time = time.time()

    for _ in range(PACKETS_PER_SECOND):
        sock.sendto(PACKET, (TARGET_IP, TARGET_PORT))

    elapsed_time = time.time() - start_time
    sleep_time = max(0, 1 - elapsed_time)  # Adjust for timing precision
    time.sleep(sleep_time)
