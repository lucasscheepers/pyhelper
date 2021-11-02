from mmpy_bot import Bot, Settings
from plugins.base import Base
from plugins.gitlab import GitLab

import os
import sys
import coloredlogs
from dotenv import load_dotenv
load_dotenv()
coloredlogs.install()

plugins = [Base(), GitLab()]


def main():
    bot = Bot(
        settings=Settings(
            MATTERMOST_URL=os.getenv('MATTERMOST_URL'),
            MATTERMOST_PORT=os.getenv('MATTERMOST_PORT'),
            BOT_TOKEN=os.getenv('BOT_TOKEN'),
            BOT_TEAM=os.getenv('BOT_TEAM'),
            SSL_VERIFY=False
        ),
        plugins=plugins
    )
    bot.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
