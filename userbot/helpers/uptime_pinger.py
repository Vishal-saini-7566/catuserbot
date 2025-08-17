import requests
from apscheduler.schedulers.background import BackgroundScheduler

from ..Config import Config

PING_URL = Config.UPTIME_PING_URL


def ping():
    try:
        r = requests.get(PING_URL, timeout=10)
        print(f"[UPTIME PINGER] Pinged {PING_URL} - Status {r.status_code}")
    except Exception as e:
        print(f"[UPTIME PINGER] Failed: {e}")


def start_uptime_pinger():
    if not PING_URL:
        print("No PING URL set, skipping uptime pinger")
        return

    scheduler = BackgroundScheduler()
    scheduler.add_job(ping, "interval", minutes=7)
    scheduler.start()
