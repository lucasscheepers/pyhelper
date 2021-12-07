from .utils_integration import OFF_TOPIC_ID
from .utils_integration import driver as driver_fixture
from .utils_integration import expect_reply

driver = driver_fixture


class TestKubernetesPlugin:
    def test_help_kubectl_get(self, driver):
        post = driver.create_post(OFF_TOPIC_ID, "kubectl get -h")
        reply = expect_reply(driver, post)

        assert reply["message"] == (
            "| COMMANDS | INFORMATION | MANDATORY ARGUMENTS | OPTIONAL ARGUMENTS\n"
            "| :-: | :-: | :-: | :-: |\n"
            "| **NOTE: ALL MANDATORY & OPTIONAL ARGUMENTS WITH IDENTIFIER ARE LIMITED TO ONE WORD**\n"
            "| namespaces | *Retrieve a list of the namespaces in the Kubernetes cluster* | *None* | *None*\n"
            "| pods | *Retrieve a list of running applications in the Kubernetes cluster* | -n, --namespace *= the "
            "name of the specific namespace* | *None*\n"
            "| logs | *Retrieve logs of a specific application* | -n, --namespace *= the name of the specific "
            "namespace* **and** -p, --pod_name *= the name of the pod* | *None*\n"
        )

    def test_kubectl_get_namespaces(self, driver):
        post = driver.create_post(OFF_TOPIC_ID, "kubectl get namespaces")
        reply = expect_reply(driver, post)

        assert reply["message"] == (
            f"Available namespaces in the Kubernetes cluster:\n- namespace1\n- namespace2\n- namespace3"
        )

    def test_kubectl_get_pods(self, driver):
        post = driver.create_post(OFF_TOPIC_ID, "kubectl get pods -n namespace1")
        reply = expect_reply(driver, post)

        assert reply["message"] == (
            f"Available pods in the namespace 'namespace1':\n- pod1\n- pod2"
        )

    def test_kubectl_get_logs(self, driver):
        post = driver.create_post(OFF_TOPIC_ID, "kubectl get logs -n namespace1 -p pod1")
        reply = expect_reply(driver, post)

        assert reply["message"] == "```2021-12-02 10:54:04 test[1] INFO Test logs```"

        post = driver.create_post(OFF_TOPIC_ID, "kubectl get logs -n namespace1 -p unknownPod")
        reply = expect_reply(driver, post)

        assert reply["message"] == (
            "An error has occurred:\n"
            f"- Error: the logs of the pod 'unknownpod' was not found in the namespace 'namespace1'. "
            f"Please check if the pod_name and namespace are correct \n"
        )
