import logging
import os

from mmpy_bot import Plugin, listen_to
from mmpy_bot import Message

log = logging.getLogger("plugins/base.py")


def error_response(error: str):
    response = (
        "An error has occurred:\n"
        f"- Error: {error}\n"
    )

    return response


class Base(Plugin):
    def on_start(self):
        """Notifies off-topic channel that the bot is now running."""

        self.driver.create_post(channel_id=os.getenv('BOT_CHNNL_ID'), message=">I've just started running!")  # TODO: ADD TO ENV FILE

    def on_stop(self):
        """Notifies off-topic channel that the bot is shutting down."""

        self.driver.create_post(channel_id=os.getenv('BOT_CHNNL_ID'), message=">I'll be right back!")  # TODO: ADD TO ENV FILE

    @listen_to("help")
    def help_pyhelper(self, message: Message):
        """Retrieves a list of all the commands & arguments including further explanation"""

        response = (
            "| COMMANDS | INFORMATION | MANDATORY ARGUMENTS | OPTIONAL ARGUMENTS\n"
            "| :-: | :-: | :-: | :-: |\n"
            "| help | *Retrieve a list of all the commands & arguments including further explanation* | *None* "
            "| *None* |\n"
            "| git create | *Create new merge requests, to-do items, roll out new releases or open new issues* "
            "| merge-request **or** release | -h *= help* |\n"
            "| git close | *Close issues or to-do items* | issue **or** to-do-item | -h *= help* |\n"
        )

        self.driver.reply_to(message, response)
        log.info(f"Sent successfully a response back to Mattermost")
