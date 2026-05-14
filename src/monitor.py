import time
import csv
from datetime import datetime

INPUT_FILE = "data/PT_Metrics.csv"
OUTPUT_FILE = "data/readings.csv"
REPORT_FILE = "data/summary_report.txt"


def get_status(latency, packet_loss, devices_online, router_up):
    if not router_up:
        return "CRITICAL"
    elif latency > 150 or packet_loss >= 6 or devices_online < 3:
        return "CRITICAL"
    elif latency > 100 or packet_loss >= 3 or devices_online < 4:
        return "WARNING"
    return "NORMAL"


def display_reading(timestamp, latency, packet_loss, devices_online, router_up, status):
    print("-" * 70)
    print(f"Time: {timestamp}")
    print(f"Latency: {latency}ms")
    print(f"Packet Loss: {packet_loss}%")
    print(f"Devices Online: {devices_online}")
    print(f"Router Up: {router_up}")
    print(f"Network Status: {status}")


def save_reading(timestamp, latency, packet_loss, devices_online, router_up, status):
    with open(OUTPUT_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow([
                "processed_time",
                "source_timestamp",
                "latency_ms",
                "packet_loss_percent",
                "devices_online",
                "router_up",
                "status"
            ])

        processed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        writer.writerow([
            processed_time,
            timestamp,
            latency,
            packet_loss,
            devices_online,
            router_up,
            status
        ])


def create_summary_report(readings):
    total = len(readings)

    if total == 0:
        print("No readings found.")
        return

    latencies = [reading["latency"] for reading in readings]

    warning_count = sum(
        1 for reading in readings
        if reading["status"] == "WARNING"
    )

    critical_count = sum(
        1 for reading in readings
        if reading["status"] == "CRITICAL"
    )

    normal_count = sum(
        1 for reading in readings
        if reading["status"] == "NORMAL"
    )

    average_latency = sum(latencies) / total
    highest_latency = max(latencies)
    lowest_latency = min(latencies)

    report = f"""
Smart Network Status Monitor - Release 2 Summary Report

Total Readings: {total}
Normal Events: {normal_count}
Warning Events: {warning_count}
Critical Events: {critical_count}

Average Latency: {average_latency:.2f}ms
Highest Latency: {highest_latency}ms
Lowest Latency: {lowest_latency}ms

Release 2 Improvements:
- Reads structured CSV data based on Packet Tracer scenarios
- Processes latency, packet loss, device count, and router status
- Produces historical summary statistics
- Creates a report file for project evidence
"""

    with open(REPORT_FILE, "w") as file:
        file.write(report)

    print("\nSummary report created:")
    print(REPORT_FILE)


def run_monitor():
    readings = []

    with open(INPUT_FILE, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            timestamp = row["timestamp"]
            latency = int(row["latency_ms"])
            packet_loss = int(row["packet_loss_percent"])
            devices_online = int(row["devices_online"])
            router_up = row["router_up"] == "True"

            status = get_status(
                latency,
                packet_loss,
                devices_online,
                router_up
            )

            display_reading(
                timestamp,
                latency,
                packet_loss,
                devices_online,
                router_up,
                status
            )

            save_reading(
                timestamp,
                latency,
                packet_loss,
                devices_online,
                router_up,
                status
            )

            readings.append({
                "latency": latency,
                "packet_loss": packet_loss,
                "devices_online": devices_online,
                "router_up": router_up,
                "status": status
            })

            time.sleep(2)

    create_summary_report(readings)


if __name__ == "__main__":
    run_monitor()