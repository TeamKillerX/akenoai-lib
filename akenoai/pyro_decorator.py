# MODULES MOD
# FULL CREDITS BY @XTDEVS
# PLEASE DO NOT REMOVE CREDITS
# COPYRIGHT 2019-2024
# REMEMBER: COPYING AND PASTING WITHOUT UNDERSTANDING WILL ONLY HURT YOUR GROWTH. RESPECT THE ORIGINAL WORK BY GIVING PROPER CREDITS AND FOLLOWING THE RULES. START LEARNING, NOT JUST COPYING!

"""
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from functools import wraps

from pyrogram import Client, filters  # type: ignore
from pyrogram.enums import ChatMemberStatus, ChatType  # type: ignore
from pyrogram.errors import *  # type: ignore
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message  # type: ignore

import akenoai.logger as akeno


def validate_channel_inputs(where_from, owner_id):
    if "https://t.me/" in where_from or "https://t.me/" in owner_id:
        raise ValueError("Don't use links: format eg: where_from='RendyProjects' and owner_id='xtdevs'")

def create_channel_button(channel):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(text="The Channel", url=f"https://t.me/{channel}")
    ]])


def ForceSubscribe(where_from=None, owner_id=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(client: Client, message: Message):
            try:
                validate_channel_inputs(where_from, owner_id)
                if await check_membership(where_from, owner_id, client, message):
                    return await func(client, message)
                mention = message.from_user.mention if message.from_user else ""
                await message.reply(
                    f"Hey {mention}\n⚠️ To use this bot you have to <b>subscribe to our channel</b>",
                    disable_web_page_preview=True,
                    reply_markup=create_channel_button(where_from)
                )
                await message.stop_propagation()
            except ChatAdminRequired as e: # type: ignore
                await akeno.warning(str(e))
            return await func(client, message)
        return wrapper
    return decorator

async def handle_banned_user(owner, mention_user, bot, msg):
    admin_button = InlineKeyboardMarkup([[
        InlineKeyboardButton(text="Developer", url=f"https://t.me/{owner}")
    ]])
    mention = mention_user.mention if mention_user else ""
    await bot.send_message(
        msg.chat.id,
        f"❌ you {mention} have been blocked from the group support\n\nclick the button below to contact the group admin",
        reply_markup=admin_button
    )
    return False

async def check_membership(channel_id, owner, bot, msg):
    try:
        user_id = msg.from_user.id if msg.from_user else 0
        mention_user = await bot.get_users(user_id)
        user = await bot.get_chat_member(channel_id, user_id)
        if user.status == ChatMemberStatus.BANNED:
            return await handle_banned_user(owner, mention_user, bot, msg)
        return True
    except UserNotParticipant: # type: ignore
        return False

def with_premium(func):
    async def wrapper(client: Client, message: Message):
        if not client.me.is_premium:
            await message.edit_text("<b>Premium account is required</b>")
        else:
            return await func(client, message)
    return wrapper

def disable_command(command=None):
    def decorator(func):
        @Client.on_message(~filters.command(command))
        async def wrapper(client: Client, message: Message):
            await func(client, message)
        return wrapper
    return decorator

def format_user_info(user, message, chat) -> str:
    if message.chat.type == ChatType.PRIVATE:
        return (
            f"UserID: {user.id if user else 0}\n"
            f"Username: {user.username if user else None}\n"
            f"First Name: {user.first_name if user else ''}\n"
        )
    elif message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return (
            f"UserID: {user.id if user else 0}\n"
            f"Username: {user.username if user else None}\n"
            f"First Name: {user.first_name if user else ''}\n"
            f"Chat Title: {chat.title if chat else ''}\n"
            f"Chat Username: {chat.username if chat else None}\n"
        )

def LogChannel(channel_id=None, is_track: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(client: Client, message: Message):
            if is_track:
                try:
                    formatting = format_user_info(message.from_user, message, message.chat)
                    if message.link:
                        if message.chat.type == ChatType.PRIVATE:
                            reply_markup = None
                        reply_markup = InlineKeyboardMarkup([[
                            InlineKeyboardButton(text="👀 Message Link", url=message.link)
                        ]])
                    else:
                        reply_markup = None
                    if message and message.text.lower() == "vcs":
                        await client.send_message(channel_id, formatting, reply_markup=reply_markup)
                    else:
                        await client.send_message(channel_id, formatting, reply_markup=reply_markup)
                except Exception as e:
                    await akeno.warning(str(e))
            else:
                return False
            return await func(client, message)
        return wrapper
    return decorator

def check_is_admin(status: bool = True):
    def decorator(func):
        @wraps(func)
        async def wrapper(client: Client, message: Message):
            if status:
                try:
                    member = await client.get_chat_member(message.chat.id, "me")
                    if member.status != ChatMemberStatus.ADMINISTRATOR:
                        return await message.reply_text("I am not an administrator in this group.")
                except Exception as e:
                    return await message.reply_text(f"Error while checking admin status: {e}")
                return await func(client, message)
            else:
                return await message.reply_text("Admin check is disabled.")
        return wrapper
    return decorator
