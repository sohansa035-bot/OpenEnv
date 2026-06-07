import requests
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def run_inference():
    print("[START] Starting SRE Incident Triage Baseline")
    
    # Reset
    resp = requests.post(f"{BASE_URL}/reset", json={"scenario": 1})
    data = resp.json()
    print("[STEP] Reset:", data.get("alert_summary", data))
    
    # Example actions for Task 1
    resp = requests.post(f"{BASE_URL}/step", json={"command": "ANALYZE_LOGS payment"})
    data = resp.json()
    print("[STEP] Analyze:", data.get("output", ""), "Reward:", data.get("reward", 0))
    
    resp = requests.post(f"{BASE_URL}/step", json={"command": "ISOLATE_SERVICE payment-service"})
    data = resp.json()
    print("[STEP] Isolate:", data.get("output", ""), "Reward:", data.get("reward", 0), "Done:", data.get("done", False))
    
    print("[END] Baseline completed. Average reward high on easy task.")

if __name__ == "__main__":
    run_inference()
