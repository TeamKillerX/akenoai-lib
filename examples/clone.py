#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2020-2024 (c) Randy @xtdevs
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import os
from asyncio import *
from random import *

from pyrogram import *
from pyrogram import Client as ren
from pyrogram.errors import RPCError
from pyrogram.types import *

CLONE_STORAGE = {}

@ren.on_message(
    ~filters.scheduled
    & filters.command(["clone"], ["."])
    & filters.me
    & ~filters.forwarded
)
async def user_clone(client: Client, message: Message):
    reply_messages = message.reply_to_message
    if not reply_messages:
        return await message.reply_text("Please reply to a message.")
    if not reply_messages.from_user:
        return await message.reply_text("Invalid user.")
    user_id = reply_messages.from_user.id if reply_messages.from_user else "@" + reply_messages.from_user.username
    try:
        me_user = await client.get_chat("me")
        me_user_two = await client.get_users("me")
        user = await client.get_chat(user_id)
        user_two = await client.get_users(user_id)
    except Exception as e:
        return await message.reply_text(f"Error: {e}")
    me_bio = me_user.bio if me_user else ""
    me_first_name = me_user.first_name if me_user else ""
    me_last_name = me_user.last_name if me_user else ""
    user_bio = user.bio if user else ""
    user_first_name = user.first_name if user else ""
    user_photo_file_id = user.photo.big_file_id if user.photo else None
    me_photo_file_id = None
    try:
        async for file in client.get_chat_photos(client.me.id, limit=1):
            me_photo_file_id = file.file_id if file else None
    except RPCError as rpc_error:
        return await message.reply_text(f"RPCError: {rpc_error}")
    except Exception as e:
        return await message.reply_text(f"Error: {e}")
    try:
        CLONE_STORAGE[me_user.id] = {
            "first_name": me_first_name,
            "last_name": me_last_name,
            "profile_id": me_photo_file_id,
            "bio_data": me_bio
        }
        set_profile = None
        if user_photo_file_id:
            set_profile = await client.download_media(user_photo_file_id)
        if set_profile:
            await client.set_profile_photo(photo=set_profile)
        if user_first_name and user_bio:
            await client.update_profile(first_name=user_first_name, last_name="", bio=user_bio)
        await message.reply_text("Successfully steal and set to your account!")
        if set_profile:
            os.remove(set_profile)
    except Exception as e:
        await message.reply_text(f"Error: {e}")

@ren.on_message(
    ~filters.scheduled
    & filters.command(["revert"], ["."])
    & filters.me
    & ~filters.forwarded
)
async def user_revert(client: Client, message: Message):
    user = await client.get_users("me")
    CLONE_STORAGE[user.id] = {
        "first_name": CLONE_STORAGE[user.id]["first_name"],
        "last_name": CLONE_STORAGE[user.id]["last_name"],
        "profile_id": CLONE_STORAGE[user.id]["profile_id"],
        "bio_data": CLONE_STORAGE[user.id]["bio_data"],
    }
    try:
        clone_data = CLONE_STORAGE.get(user.id)
        photos = [p async for p in client.get_chat_photos("me")]
        if photos:
            await client.delete_profile_photos(photos[0].file_id)
        if clone_data["first_name"]:
            await client.update_profile(
                first_name=clone_data["first_name"],
                last_name=clone_data["last_name"],
                bio=clone_data["bio_data"]
            )
        else:
            return await message.reply_text("User doesn't have a profile bio and last name")
        await message.reply_text("Successfully reverted back to your account!")
        del CLONE_STORAGE[user.id]
    except RPCError as rpc_error:
        await message.reply_text(f"RPCError: {rpc_error}")
    except Exception as e:
        await message.reply_text(f"Error: {e}")
