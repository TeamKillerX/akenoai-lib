#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Credits @xpushz on telegram 
# Copyright 2020-2025 (c) Randy W @xtdevs, @xtsea on telegram
#
# from : https://github.com/TeamKillerX
# Channel : @RendyProjects
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import json
import os
import time
import subprocess
from datetime import datetime

import requests
import streamlit
from box import Box
from streamlit_option_menu import option_menu

import akenoai.logger as fast

class SendWaifuRandom:
    def __init__(self):
        pass

    def send_waifu_pics(self, waifu_category):
        waifu_api = "https://api.waifu.pics/sfw"
        waifu_param = f"{waifu_api}/{waifu_category}"
        response = requests.get(waifu_param)
        if response.status_code != 200:
            return "Sorry, there was an error processing your request. Please try again later"
        data_waifu = response.json()
        try:
            waifu_image_url = data_waifu["url"]
        except Exception as e:
            return f"Error request {e}"
        if waifu_image_url:
            try:
                return waifu_image_url
            except Exception:
                return f"**Info Error:**"
        else:
            return "Not found waifu"

class StreamlitJs:
    def __init__(self):
        self.public_url = "https://randydev-ryu-js.hf.space"
        self.obj = Box
        self.st = streamlit

    def stl(self):
        return self.st

    def waifu_random(self):
        js_st = self.stl()
        js_st.title("Waifu Random")
        js_st.write("Developer by RandyDev")
        with js_st.form('waifu-random'):
            text = js_st.text_area('Enter text:', 'neko')
            submitted = js_st.form_submit_button('Submit')
            placeholder = js_st.empty()
            if submitted and not (text.startswith(("neko", "waifu", "megumin"))):
                js_st.warning("Unsupported waifu format. Please enter a valid waifu text", icon="⚠")
            elif submitted and text.startswith(("neko", "waifu", "megumin")):
                send_image = SendWaifuRandom().send_waifu_pics(text)
                try:
                    if send_image:
                        with placeholder, js_st.spinner("Processing......"):
                            time.sleep(5)
                        js_st.image(send_image, caption="Powered by akenoai-lib")
                        js_st.success("Join Channel telegram : @RendyProjects")
                    else:
                        js_st.error("Error: Unable to waifu random for the given text.")
                except Exception as e:
                    js_st.error(f"Error: {e}")

    def set_page_config(self, **args):
        self.st.set_page_config(**args)

    def app_option_menu(self, **args):
        return option_menu(**args)

    def javascript_code(self, streamlit_style, unsafe_allow_html=False):
        self.st.markdown(streamlit_style, unsafe_allow_html=unsafe_allow_html)

    def hide_streamlit_watermark(self, unsafe_allow_html=False):
        hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .css-1rs6os {visibility: hidden;}
        .css-17ziqus {visibility: hidden;}
        </style>
        """
        self.st.markdown(hide_streamlit_style, unsafe_allow_html=unsafe_allow_html)
        self.st.header("")

    def dict_to_obj(self, func):
        return self.obj(func or {})

    def _prepare_request(self, endpoint, api_key=None):
        """Prepare common request parameters and validate API key."""
        if not api_key:
            api_key = os.environ.get("AKENOX_KEY")
        if not api_key:
            raise ValueError("Required variables AKENOX_KEY or api_key")
        url = f"{self.public_url}/api/v1/{endpoint}"
        headers = {"x-api-key": api_key}
        return url, headers

    def _make_request_in(self, endpoint, api_key=None, post=False, verify=False, **params):
        url, headers = self._prepare_request(endpoint, api_key)
        try:
            if post:
                response = requests.post(url, headers=headers, params=params, verify=verify)
                return response.json() if endpoint != "maker/carbon" else response.content
            else:
                response = requests.get(url, headers=headers, params=params, verify=verify)
                return response.json() if endpoint != "maker/carbon" else response.content
        except json.decoder.JSONDecodeError:
            raise Exception("GET OR POST INVALID: check problem, invalid json")
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to host")
        except Exception as e:
            return str(e)

    @fast.no_async_log_performance
    def no_async_randydev(
        self,
        endpoint,
        api_key=None,
        post=False,
        is_obj=False,
        verify=True,
        **params
    ):
        if is_obj:
            return Box(self._make_request_in(endpoint, api_key, post=post, verify=verify, **params) or {})
        else:
            return self._make_request_in(endpoint, api_key, post=post, verify=verify, **params)

StreamlitToJs = StreamlitJs()
