import logging
import os
from datetime import datetime
import pytz

from mmpy_bot import Plugin, listen_to
from mmpy_bot import Message

log = logging.getLogger("plugins/base.py")


def error_response(error: str):
    response = (
        "An error has occurred:\n"
        f"- Error: {error}\n"
    )

    return response


class BaseP(Plugin):
    def on_start(self):
        """Notifies off-topic channel that the bot is now running."""
        europe_dt = datetime.now().astimezone(pytz.timezone("Europe/Amsterdam")).strftime('%H:%M:%S')

        self.driver.create_post(channel_id=os.getenv('BOT_CHNNL_ID'), message=">I've just started running at "
                                                                              f"{europe_dt}!")

    @listen_to("help")
    def help_pyhelper(self, message: Message):
        """Retrieves a list of all the commands & arguments including further explanation"""

        response = (
            "| COMMANDS | INFORMATION | MANDATORY ARGUMENTS | OPTIONAL ARGUMENTS\n"
            "| :-: | :-: | :-: | :-: |\n"
            "| help | *Retrieve a list of all the commands & arguments including further explanation* | *None* "
            "| *None* |\n"
            "| git create | *Create new merge requests, roll out new releases or open new issues* "
            "| merge-request **or** release **or** issue **or** -h *= help* | *None* |\n"
            "| git close | *Close issues* | issue **or** -h *= help* | *None* |\n"
            "| kubectl get | *Retrieve a list of the namespaces or running applications in the Kubernetes cluster or "
            "logs of a specific application* | namespaces **or** pods **or** logs **or** -h *= help* | *None* |\n"
        )

        self.driver.reply_to(message, response)
        log.info(f"Sent successfully a response back to Mattermost")
