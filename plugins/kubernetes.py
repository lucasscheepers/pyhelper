import logging
import os
import click
from mmpy_bot import Plugin, listen_to
from mmpy_bot import Message
import plugins.base
from exceptions.logs_not_found_exceptions import LogsNotFound
from services.kubernetes_service import KubernetesService

log = logging.getLogger("plugins/kubernetes.py")


class Kubernetes(Plugin):
    def __init__(self):
        super().__init__()
        if os.getenv("DISABLE_KUBERNETES_SERVICE") == "False":
            self.kubernetes_service = KubernetesService()

    @listen_to("kubectl get -h")
    def help_kubectl_get(self, message: Message):
        """Retrieves a list of all 'kubectl get' commands & arguments including further explanation"""
        response = (
            "| COMMANDS | INFORMATION | MANDATORY ARGUMENTS | OPTIONAL ARGUMENTS\n"
            "| :-: | :-: | :-: | :-: |\n"
            "| **NOTE: ALL MANDATORY & OPTIONAL ARGUMENTS WITH IDENTIFIER ARE LIMITED TO ONE WORD**\n"
            "| namespaces | *Retrieve a list of the namespaces in the Kubernetes cluster* | *None* | *None*\n"
            "| pods | *Retrieve a list of running applications in the Kubernetes cluster* | -n, --namespace *= the "
            "name of the specific namespace* | *None*\n"
            "| logs | *Retrieve logs of a specific application* | -n, --namespace *= the name of the specific "
            "namespace* **and** -p, --pod_name *= the name of the pod* | *None*\n"
        )

        self.driver.reply_to(message, response)
        log.info(f"Sent successfully a response back to Mattermost")

    @listen_to("kubectl get namespaces")
    def kubectl_get_namespaces(
            self, message: Message
    ):
        """Retrieves a list of the namespaces in the Kubernetes cluster"""
        try:
            namespaces_arr = self.kubernetes_service.get_namespaces()
            namespaces = "- " + "\n- ".join(namespaces_arr)

            response = (
                f"Available namespaces in the Kubernetes cluster:\n"
                f"{namespaces}"
            )

            self.driver.reply_to(message, response)
            log.info(f"Sent successfully a response back to Mattermost")
        except Exception as e:
            self.driver.reply_to(message, plugins.base.error_response(str(e)))
            log.error(f"An error has occured: {str(e).lower()}")

    @listen_to("kubectl get pods")
    @click.command(help="Retrieves a list of running applications in the Kubernetes cluster")
    @click.option("-n", "--namespace", type=str, help="The name of the namespace")
    def kubectl_get_pods(
            self, message: Message, namespace: str
    ):
        """Retrieves a list of running applications in the Kubernetes cluster"""
        try:
            body = {
                'event_type': 'get_pods',
                'namespace': namespace,
            }
            pods_arr = self.kubernetes_service.get_pods(body)
            pods = "- " + "\n- ".join(pods_arr)

            response = f"No resources found in the namespace '{namespace}'" if not pods_arr else (
                f"Available pods in the namespace '{namespace}':\n"
                f"{pods}"
            )

            self.driver.reply_to(message, response)
            log.info(f"Sent successfully a response back to Mattermost")
        except Exception as e:
            self.driver.reply_to(message, plugins.base.error_response(str(e)))
            log.error(f"An error has occured: {str(e).lower()}")

    @listen_to("kubectl get logs")
    @click.command(help="Retrieve logs of a specific application")
    @click.option("-n", "--namespace", type=str, help="The name of the namespace")
    @click.option("-p", "--pod_name", type=str, help="The name of the pod")
    def kubectl_get_logs(
            self, message: Message, namespace: str, pod_name: str
    ):
        """Retrieve logs of a specific application"""
        try:
            body = {
                'event_type': 'get_logs',
                'namespace': namespace,
                'pod_name': pod_name
            }
            logs = self.kubernetes_service.get_logs(body)

            response = f'```{logs}```'

            self.driver.reply_to(message, response)
            log.info(f"Sent successfully a response back to Mattermost")
        except LogsNotFound as e:
            self.driver.reply_to(message, plugins.base.error_response(f"{str(e).lower()}. Please check if the pod_name "
                                                                      f"and namespace are correct "))
            log.error(f"An error has occured: {str(e).lower()}. "
                      "Please check if the pod_name and namespace are correct")
