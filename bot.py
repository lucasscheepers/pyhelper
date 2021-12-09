from mmpy_bot import Bot, Settings
from plugins.base import Base
from plugins.gitlab import GitLab
from plugins.kubernetes import Kubernetes

import os
import logging
import coloredlogs
from dotenv import load_dotenv

if os.getenv('TESTING') == "True":
    load_dotenv(".testing-env")
else:
    load_dotenv()

coloredlogs.install()

log = logging.getLogger("bot.py")

plugins = [Base(), GitLab(), Kubernetes()]


def main():
    bot = Bot(
        settings=Settings(
            MATTERMOST_URL=os.getenv('MATTERMOST_URL'),
            MATTERMOST_PORT=os.getenv('MATTERMOST_PORT'),
            BOT_TOKEN=os.getenv('BOT_TOKEN'),
            BOT_TEAM=os.getenv('BOT_TEAM'),
            SSL_VERIFY=True
        ),
        plugins=plugins
    )
    bot.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log.info(f"PyHelper stopped")
