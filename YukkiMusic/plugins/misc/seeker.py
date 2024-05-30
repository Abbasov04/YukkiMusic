#
# Copyright (C) 2024-present by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#
import asyncio

from pyrogram.types import InlineKeyboardMarkup

from strings import get_string
from YukkiMusic.misc import db
from YukkiMusic.utils.database import get_active_chats, get_lang, is_music_playing
from YukkiMusic.utils.formatters import seconds_to_min
from YukkiMusic.utils.inline import stream_markup_timer, telegram_markup_timer

from ..admins.callback import wrong

checker = {}


async def timer():
    while not await asyncio.sleep(1):
        active_chats = await get_active_chats()
        for chat_id in active_chats:
            if not await is_music_playing(chat_id):
                continue
            playing = db.get(chat_id)
            if not playing:
                continue
            file_path = playing[0]["file"]
            if "index_" in file_path or "live_" in file_path:
                continue
            duration = int(playing[0]["seconds"])
            if duration == 0:
                continue
            db[chat_id][0]["played"] += 1


asyncio.create_task(timer())


async def markup_timer():
    while not await asyncio.sleep(2):
        active_chats = await get_active_chats()
        for chat_id in active_chats:
            try:
                if not await is_music_playing(chat_id):
                    continue
                playing = db.get(chat_id)
                if not playing:
                    continue
                duration_seconds = int(playing[0]["seconds"])
                if duration_seconds == 0:
                    continue
                try:
                    mystic = playing[0]["mystic"]
                    markup = playing[0]["markup"]
                except:
                    continue
                try:
                    check = wrong[chat_id][mystic.message_id]
                    if check is False:
                        continue
                except:
                    pass
                try:
                    language = await get_lang(chat_id)
                    _ = get_string(language)
                except:
                    _ = get_string("en")
                try:
                    buttons = (
                        stream_markup_timer(
                            _,
                            playing[0]["vidid"],
                            chat_id,
                            seconds_to_min(playing[0]["played"]),
                            playing[0]["dur"],
                        )
                        if markup == "stream"
                        else telegram_markup_timer(
                            _,
                            chat_id,
                            seconds_to_min(playing[0]["played"]),
                            playing[0]["dur"],
                        )
                    )
                    await mystic.edit_reply_markup(
                        reply_markup=InlineKeyboardMarkup(buttons)
                    )
                except:
                    continue
            except:
                continue


asyncio.create_task(markup_timer())


from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import LOG_GROUP_ID
from YukkiMusic import app
from YukkiMusic.utils.database import get_served_users

if app.username == "YukkiMusic_vkBot":
    AUTO_GCASTS = True
    AUTO_GCAST = True
else:
    AUTO_GCASTS = False
    AUTO_GCAST = False
START_IMG_URLS = "https://graph.org/file/497d715b03115857db6d8.jpg"

MESSAGES = f"""‣  тнιѕ ιѕ {app.mention}

➜ α мυѕιᴄ ρℓαуєʀ вσт ωιтн ѕσмє α∂ναиᴄє∂ fєαтυʀєѕ."""


BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "𝙰𝚍𝚍 𝙼𝚎", url=f"https://t.me/YukkiMusic_vkBot?startgroup=true"
            )
        ]
    ]
)


TEXT = """ᴀᴜᴛᴏ ɢᴄᴀsᴛ ɪs ᴇɴᴀʙʟᴇᴅ sᴏ ᴀᴜᴛᴏ ɢᴄᴀsᴛ/ʙʀᴏᴀᴅᴄᴀsᴛ ɪs ᴅᴏɪɴ ɪɴ ᴀʟʟ ᴄʜᴀᴛs ᴄᴏɴᴛɪɴᴜᴏᴜsʟʏ. \nɪᴛ ᴄᴀɴ ʙᴇ sᴛᴏᴘᴘᴇᴅ ʙʏ ᴘᴜᴛ ᴠᴀʀɪᴀʙʟᴇ [ᴀᴜᴛᴏ_ɢᴄᴀsᴛ = (ᴋᴇᴇᴘ ʙʟᴀɴᴋ & ᴅᴏɴᴛ ᴡʀɪᴛᴇ ᴀɴʏᴛʜɪɴɢ)]"""


async def send_text_once():
    try:
        await app.send_message(LOG_GROUP_ID, TEXT)
    except Exception as e:
        pass


async def send_message_to_chats():
    try:
        chats = await get_served_users()

        for chat_info in chats:
            chat_id = chat_info.get("chat_id")
            if isinstance(chat_id, int):  # Check if chat_id is an integer
                try:
                    await app.send_photo(
                        chat_id,
                        photo=START_IMG_URLS,
                        caption=MESSAGES,
                        reply_markup=BUTTONS,
                    )
                    await asyncio.sleep(
                        20
                    )  # Sleep for 100 second between sending messages
                except Exception as e:
                    pass  # Do nothing if an error occurs while sending message
    except Exception as e:
        pass  # Do nothing if an error occurs while fetching served chats


async def continuous_broadcast():
    await send_text_once()  # Send TEXT once when bot starts

    while True:
        if AUTO_GCAST:
            try:
                await send_message_to_chats()
            except Exception as e:
                pass

        # Wait for 100000 seconds before next broadcast
        await asyncio.sleep(3600)


# Start the continuous broadcast loop if AUTO_GCAST is True
if AUTO_GCAST:
    asyncio.create_task(continuous_broadcast())
