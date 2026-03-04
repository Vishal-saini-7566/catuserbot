# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import random
import re
import time
from datetime import datetime
from platform import python_version

import requests
from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from userbot import StartTime, catub, catversion

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import mention

plugin_category = "utils"

ANIME_QUOTE = [
    "✮ One’s act, one’s profit 🖤",
    "✮ Ten men, ten colors 🖤",
    "✮ Wake from death and return to life 🖤",
    "✮ Evil cause, evil effect 🖤",
    "✮ The weak are meat; the strong eat 🖤",
    "✮ Drunken life, dreamy death 🖤",
    "✮ One life, one encounter  🖤",
    "✮ Different body, same mind 🖤",
    "✮ Meeting person always separated 🖤",
    "✮ Beautiful person, thin life 🖤",
    "✮ Work of self, obtainment of self 🖤",
    "✮ If you do not enter the tiger’s cave, you will not catch its cub  🖤",
    "✮ Even monkeys fall from trees 🖤",
    "✮ There are even bugs that eat knotweed 🖤",
    "✮ Spilt water will not return to the tray 🖤",
    "✮ Gold coins to a cat 🖤",
    "✮ A frog in a well does not know the great sea 🖤",
    "✮ One who chases after two hares won’t catch even one 🖤",
    "✮ An apprentice near a temple will recite the scriptures untaught  🖤",
    "✮ Fall down seven times, stand up eight 🖤",
    "✮ Unless an idiot dies, he won’t be cured 🖤",
    "✮ Give up on your dreams and die 🖤",
]

@catub.cat_cmd(
    pattern="alive$",
    command=("alive", plugin_category),
    info={
        "header": "To check bot's alive status",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    reply_to_id = await reply_id(event)
    ANIME = None
    cat_caption = gvarstatus("ALIVE_TEMPLATE") or temp
    if "ANIME" in cat_caption:
        data = requests.get("https://animechan.vercel.app/api/random").json()
        ANIME = f"**“{data['quote']}” - {data['character']} ({data['anime']})**"
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    catevent = await edit_or_reply(event, "`Checking...`")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or " ✧✧ "
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or f"{random.choice(ANIME_QUOTE)}"
    CAT_IMG = gvarstatus("ALIVE_PIC")
    caption = cat_caption.format(
        ALIVE_TEXT=ALIVE_TEXT,
        ANIME=ANIME,
        EMOJI=EMOJI,
        mention=mention,
        uptime=uptime,
        telever=version.__version__,
        catver=catversion,
        pyver=python_version(),
        dbhealth=check_sgnirts,
        ping=ms,
    )
    if CAT_IMG:
        CAT = list(CAT_IMG.split())
        PIC = random.choice(CAT)
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=caption, reply_to=reply_to_id
            )
            await catevent.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                catevent,
                f"**Media Value Error!!**\n__Change the link by __`.setdv`\n\n**__Can't get media from this link :-**__ `{PIC}`",
            )
    else:
        await edit_or_reply(
            catevent,
            caption,
        )


temp = """{ALIVE_TEXT}
**{EMOJI} Database :** `{dbhealth}`
**{EMOJI} Telethon Version :** `{telever}`
**{EMOJI} Catuserbot Version :** `{catver}`
**{EMOJI} Python Version :** `{pyver}`
**{EMOJI} Uptime :** `{uptime}`
**{EMOJI} Master:** {mention}"""


def catalive_text():
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  ✥ "
    cat_caption = "**Catuserbot is Up and Running**\n"
    cat_caption += f"**{EMOJI} Telethon version :** `{version.__version__}\n`"
    cat_caption += f"**{EMOJI} Catuserbot Version :** `{catversion}`\n"
    cat_caption += f"**{EMOJI} Python Version :** `{python_version()}\n`"
    cat_caption += f"**{EMOJI} Master:** {mention}\n"
    return cat_caption


@catub.cat_cmd(
    pattern="ialive$",
    command=("ialive", plugin_category),
    info={
        "header": "To check bot's alive status via inline mode",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}ialive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, "ialive")
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@catub.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await catalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
