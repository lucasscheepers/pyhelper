import time
from typing import Dict

import pytest

from mmpy_bot import (
    Bot,
    Settings
)
from mmpy_bot.driver import Driver

OFF_TOPIC_ID = "ahzqezf33jny9mpst758dnaahw"
RESPONSE_TIMEOUT = 15


def expect_reply(driver: Driver, post: Dict, wait=RESPONSE_TIMEOUT, retries=1):
    """Utility function to specify we expect some kind of reply after `wait` seconds."""
    reply = None
    for _ in range(retries + 1):
        time.sleep(wait)
        thread_info = driver.get_thread(post["id"])
        reply_id = thread_info["order"][-1]
        if reply_id != post["id"]:
            reply = thread_info["posts"][reply_id]
            break

    if not reply:
        raise ValueError("Expected a response, but didn't get any!")

    return reply


@pytest.fixture(scope="session")
def driver():
    return Bot(
        settings=Settings(
            MATTERMOST_URL="http://127.0.0.1",
            BOT_TOKEN="7arqwr6kzibc58zomct9ndfk1e",
            MATTERMOST_PORT=8065,
            SSL_VERIFY=False
        ),
        plugins=[],  # We only use this bot to send messages, not to reply to anything.
    ).driver
