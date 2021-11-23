import asyncio
import re
from unittest import mock

from mmpy_bot import Message
from plugins.base import Base

from mmpy_bot.driver import Driver


def create_message(
        text="hello",
        mentions=["qmw86q7qsjriura9jos75i4why"],
        channel_type="O",
        sender_name="betty",
):
    return Message(
        {
            "event": "posted",
            "data": {
                "channel_display_name": "Off-Topic",
                "channel_name": "off-topic",
                "channel_type": channel_type,
                "mentions": mentions,
                "post": {
                    "id": "wqpuawcw3iym3pq63s5xi1776r",
                    "create_at": 1533085458236,
                    "update_at": 1533085458236,
                    "edit_at": 0,
                    "delete_at": 0,
                    "is_pinned": "False",
                    "user_id": "131gkd5thbdxiq141b3514bgjh",
                    "channel_id": "4fgt3n51f7ftpff91gk1iy1zow",
                    "root_id": "",
                    "parent_id": "",
                    "original_id": "",
                    "message": text,
                    "type": "",
                    "props": {},
                    "hashtags": "",
                    "pending_post_id": "",
                },
                "sender_name": sender_name,
                "team_id": "au64gza3iint3r31e7ewbrrasw",
            },
            "broadcast": {
                "omit_users": "None",
                "user_id": "",
                "channel_id": "4fgt3n51f7ftpff91gk1iy1zow",
                "team_id": "",
            },
            "seq": 29,
        }
    )


class TestBasePlugin:
    def test_initialize(self):
        p = Base().initialize(Driver())
        # Test whether the non-click-command is registered properly
        assert p.message_listeners[re.compile("help")] == [
            Base.help_pyhelper,
        ]

    @mock.patch("mmpy_bot.driver.ThreadPool.add_task")
    def test_help_pyhelper(self, add_task):
        p = Base().initialize(Driver())

        message = create_message(text="help")
        asyncio.run(
            p.call_function(Base.help_pyhelper, message)
        )

        add_task.assert_called_once_with(
            Base.help_pyhelper, message
        )
