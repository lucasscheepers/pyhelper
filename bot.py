from mmpy_bot import Bot, Settings
from plugins.base_plugin import BaseP
from plugins.gitlab_plugin import GitLabP
from plugins.kubernetes_plugin import KubernetesP

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

plugins = [BaseP(), GitLabP(), KubernetesP()]


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
