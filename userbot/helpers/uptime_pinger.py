import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from userbot import LOGS

from ..Config import Config

PING_URL = Config.UPTIME_PING_URL


async def ping():
    """Async ping function to avoid blocking"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(PING_URL, timeout=10) as response:
                LOGS.info(f"[UPTIME PINGER] Pinged {PING_URL} - Status {response.status}")
    except Exception as e:
        LOGS.info(f"[UPTIME PINGER] Failed: {e}")


def start_uptime_pinger():
    if not PING_URL:
        LOGS.info("No PING URL set, skipping uptime pinger")
        return

    LOGS.info("[UPTIME PINGER] Initiated")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(ping, "interval", minutes=1)
    scheduler.start()
    return scheduler
