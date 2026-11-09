
from datetime import datetime

# SecureNova Blue Team - Anomaly Detection Lab

def detect_anomalies(event):
    alerts = []

    # Scenario 1: Repeated failed login attempts
    if event.get("failed_logins", 0) >= 5:
        alerts.append(
            "BRUTE FORCE ALERT: 5 or more failed login attempts detected."
        )

    # Scenario 2: Login from an untrusted IP
    trusted_ips = ["127.0.0.1", "10.0.11.126"]

    if event.get("ip_address") not in trusted_ips:
        alerts.append(
            f"UNUSUAL IP ALERT: Access detected from {event.get('ip_address')}."
        )

    # Scenario 3: Abnormally high request rate
    if event.get("requests_per_minute", 0) > 100:
        alerts.append(
            "HIGH REQUEST RATE ALERT: More than 100 requests per minute."
        )

    return alerts


if __name__ == "__main__":

    print("=" * 65)
    print("       SECURENOVA - BLUE TEAM ANOMALY DETECTION")
    print("=" * 65)

    # Controlled test event: Scenario 1
    test_event = {
        "agent_id": "agent-worker-02",
        "ip_address": "127.0.0.1",
        "failed_logins": 7,
        "requests_per_minute": 20
    }

    print("\nAnalyzing security event...")
    print("Agent ID:", test_event["agent_id"])
    print("Failed logins:", test_event["failed_logins"])
    print("IP address:", test_event["ip_address"])
    print("Requests per minute:", test_event["requests_per_minute"])

    alerts = detect_anomalies(test_event)

    if alerts:
        print("\n[SECURITY ALERT DETECTED]")
        for alert in alerts:
            print("[ALERT]", alert)
        print("\nStatus: SUSPICIOUS ACTIVITY DETECTED")
    else:
        print("\nStatus: NORMAL - No anomalies detected")

    print("\nDetection completed at:", datetime.now().isoformat(timespec="seconds"))
    print("=" * 65)
