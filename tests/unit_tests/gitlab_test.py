import asyncio
import re
from unittest import mock

from tests.unit_tests.base_test import create_message
from plugins.gitlab_plugin import GitLabP

from mmpy_bot.driver import Driver


class TestGitLabPlugin:
    def test_initialize(self):
        p = GitLabP().initialize(Driver())
        # Test whether the non-click-commands is registered properly
        assert p.message_listeners[re.compile("git create -h")] == [
            GitLabP.help_git_create,
        ]
        assert p.message_listeners[re.compile("git close -h")] == [
            GitLabP.help_git_close,
        ]

    @mock.patch("mmpy_bot.driver.ThreadPool.add_task")
    def test_help_git_create(self, add_task):
        p = GitLabP().initialize(Driver())

        message = create_message(text="git create -h")
        asyncio.run(
            p.call_function(GitLabP.help_git_create, message)
        )

        add_task.assert_called_once_with(
            GitLabP.help_git_create, message
        )

    @mock.patch("mmpy_bot.driver.ThreadPool.add_task")
    def test_help_git_close(self, add_task):
        p = GitLabP().initialize(Driver())

        message = create_message(text="git close -h")
        asyncio.run(
            p.call_function(GitLabP.help_git_close, message)
        )

        add_task.assert_called_once_with(
            GitLabP.help_git_close, message
        )
