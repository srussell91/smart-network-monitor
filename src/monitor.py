import time
import csv
import random
from datetime import datetime

LOG_FILE = "data/readings.csv"

def get_network_data():
    latency = random.randint(10, 180)
    devices_online = random.randint(2, 6)
    router_up = random.choice([True, True, True, False])
    return latency, devices_online, router_up

def get_status(latency, devices_online, router_up):
    if not router_up:
        return "CRITICAL"
    elif latency > 120 or devices_online < 3:
        return "WARNING"
    return "NORMAL"

with open(LOG_FILE, "a", newline="") as file:
    writer = csv.writer(file)

    if file.tell() == 0:
        writer.writerow(["timestamp", "latency_ms", "devices_online", "router_up", "status"])

    while True:
        latency, devices_online, router_up = get_network_data()
        status = get_status(latency, devices_online, router_up)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[{timestamp}] Latency: {latency}ms | Devices: {devices_online} | Router: {router_up} | Status: {status}")

        writer.writerow([timestamp, latency, devices_online, router_up, status])
        file.flush()

        time.sleep(5)