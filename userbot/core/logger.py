import logging

logging.basicConfig(
    format="[%(levelname)s- %(asctime)s]- %(name)s- %(message)s",
    handlers=[logging.FileHandler("catub.log"), logging.StreamHandler()],
    level=logging.INFO,
    datefmt="%H:%M:%S",
)

logging.getLogger("telethon.client.updates").setLevel(logging.WARNING)
logging.getLogger("telethon.network").setLevel(logging.WARNING)
