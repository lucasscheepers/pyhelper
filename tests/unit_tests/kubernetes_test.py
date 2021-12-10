import asyncio
import re
from unittest import mock

from tests.unit_tests.base_test import create_message
from plugins.kubernetes_plugin import KubernetesP

from mmpy_bot.driver import Driver


class TestKubernetesPlugin:
    def test_initialize(self):
        p = KubernetesP().initialize(Driver())
        # Test whether the non-click-command is registered properly
        assert p.message_listeners[re.compile("kubectl get -h")] == [
            KubernetesP.help_kubectl_get,
        ]

    @mock.patch("mmpy_bot.driver.ThreadPool.add_task")
    def test_help_kubectl_get(self, add_task):
        p = KubernetesP().initialize(Driver())

        message = create_message(text="git create -h")
        asyncio.run(
            p.call_function(KubernetesP.help_kubectl_get, message)
        )

        add_task.assert_called_once_with(
            KubernetesP.help_kubectl_get, message
        )
