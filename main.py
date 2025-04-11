import eel
from scapy.all import sniff, wrpcap
import time

# Initialize Eel (web UI directory)
eel.init('web')

TARGET_IPS = []
THRESHOLD = 50
PACKETS = []
capturing = False  # Controls packet sniffing

@eel.expose
def set_ips(ips):
    """Set IPs from GUI input."""
    global TARGET_IPS
    TARGET_IPS = [ip.strip() for ip in ips.split(',')]
    eel.showMessage(f"Tracking IPs: {', '.join(TARGET_IPS)}")

@eel.expose
def start_capture():
    """Notify user & begin packet capture."""
    global capturing
    if not TARGET_IPS:
        eel.showMessage("Error: No IPs provided. Set IPs first!")
        return
    
    capturing = True
    eel.showMessage("Capturing packets...")
    capture_packets()

@eel.expose
def stop_capture():
    """Stops packet capturing."""
    global capturing
    capturing = False
    eel.showMessage("Monitoring stopped!")

def packet_handler(packet):
    """Capture packets based on user-defined IPs."""
    if packet.haslayer("IP") and packet["IP"].src in TARGET_IPS:
        PACKETS.append(packet)

def capture_packets():
    """Monitor packet flow dynamically."""
    global PACKETS
    prev_count = 0
    
    while capturing:
        PACKETS = []
        start_time = time.time()

        if TARGET_IPS:
            filter_exp = " or ".join([f"src {ip}" for ip in TARGET_IPS])
            sniff(filter=f"ip and ({filter_exp})", prn=packet_handler, timeout=1)
        
        packet_count = len(PACKETS)
        eel.updatePacketRate(packet_count)

        if packet_count < THRESHOLD and prev_count >= THRESHOLD:
            wrpcap("captured_packets.pcap", PACKETS)
            eel.notifyThresholdHit()

        prev_count = packet_count
        time.sleep(1)

eel.start("index.html")
