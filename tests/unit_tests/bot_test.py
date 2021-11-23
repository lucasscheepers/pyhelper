from unittest import mock

import pytest
import os

from mmpy_bot import Bot, Settings
from plugins.gitlab import GitLab
from plugins.kubernetes import Kubernetes


@pytest.fixture(scope="function")
def bot():
    bot = Bot(plugins=[GitLab(), Kubernetes()], settings=Settings(DEBUG=True))
    yield bot
    bot.stop()  # if the bot was started, stop it


class TestBot:
    @mock.patch.dict(os.environ, {"DISABLE_RABBIT": "True", "DISABLE_KUBERNETES_SERVICE": "True"})
    @mock.patch("mmpy_bot.driver.Driver.login")
    def test_init(self, login):
        # Create some plugins and mock their initialize method so we can check calls
        plugins = [GitLab(), Kubernetes()]
        for plugin in plugins:
            plugin.initialize = mock.MagicMock()

        # Create a bot and verify that it gets initialized correctly
        bot = Bot(
            settings=Settings(MATTERMOST_URL="mm-iv.nl", BOT_TOKEN="a22bed02-b7bb-4194-bbc2-7c9539aa2b2b"),
            plugins=plugins,
        )
        assert bot.driver.options["url"] == "mm-iv.nl"
        assert bot.driver.options["token"] == "a22bed02-b7bb-4194-bbc2-7c9539aa2b2b"
        assert bot.plugins == plugins
        login.assert_called_once()

        # Verify that all of the passed plugins were initialized
        for plugin in plugins:
            assert plugin.initialize.called_once_with(bot.driver)

    @mock.patch.multiple("mmpy_bot.Plugin", on_start=mock.DEFAULT, on_stop=mock.DEFAULT)
    def test_run(self, bot, **mocks):
        with mock.patch.object(bot.driver, "init_websocket") as init_websocket:
            bot.run()
            init_websocket.assert_called()

            for plugin in bot.plugins:
                plugin.on_start.assert_called()

            bot.stop()

            for plugin in bot.plugins:
                plugin.on_start.assert_called()
