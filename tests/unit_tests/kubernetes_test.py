import asyncio
import re
from unittest import mock

from tests.unit_tests.base_test import create_message
from plugins.kubernetes import Kubernetes

from mmpy_bot.driver import Driver


class TestKubernetesPlugin:
    def test_initialize(self):
        p = Kubernetes().initialize(Driver())
        # Test whether the non-click-command is registered properly
        assert p.message_listeners[re.compile("kubectl get -h")] == [
            Kubernetes.help_kubectl_get,
        ]

    @mock.patch("mmpy_bot.driver.ThreadPool.add_task")
    def test_help_kubectl_get(self, add_task):
        p = Kubernetes().initialize(Driver())

        message = create_message(text="git create -h")
        asyncio.run(
            p.call_function(Kubernetes.help_kubectl_get, message)
        )

        add_task.assert_called_once_with(
            Kubernetes.help_kubectl_get, message
        )
