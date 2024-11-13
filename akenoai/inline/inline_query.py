# created class by @xtdevs

from pyrogram.types import *
from pyrogram.enums import ParseMode

class BuilderInline:
    @classmethod
    def send_text_inline(cls, inline_text, **args):
        answers = [
            InlineQueryResultArticle(
                title="Inline text!",
                thumb_url="https://telegra.ph//file/586a3867c3e16ca6bb4fa.jpg",
                input_message_content=InputTextMessageContent(
                    message_text=inline_text,
                    parse_mode=ParseMode.DEFAULT,
                    disable_web_page_preview=True
                ),
                **args
            )
        ]
        return answers

    @classmethod
    def send_photo_inline(cls, photo_url, **args):
        answers = [
            InlineQueryResultPhoto(
                photo_url=photo_url,
                title="Photo inline!",
                thumb_url="https://telegra.ph//file/586a3867c3e16ca6bb4fa.jpg",
                **args
            )
        ]
        return answers

    @classmethod
    def send_video_inline(cls, video_url, **args):
        answers = [
            InlineQueryResultVideo(
                video_url=video_url,
                title="Video inline!",
                thumb_url="https://telegra.ph//file/586a3867c3e16ca6bb4fa.jpg",
                **args
            )
        ]
        return answers

    @classmethod
    def send_audio_inline(cls, audio_url, **args):
        answers = [
            InlineQueryResultAudio(
                audio_url=audio_url,
                title="Audio Inline!",
                thumb_url="https://telegra.ph//file/586a3867c3e16ca6bb4fa.jpg",
                **args
            )
        ]
        return answers
