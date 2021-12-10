from exceptions.logs_not_found_exception import LogsNotFoundE
import logging

log = logging.getLogger("services/mock_kubernetes_service.py")


class MockKubernetesService:
    def get_namespaces(self):
        return ["namespace1", "namespace2", "namespace3"]

    def get_pods(self, body):
        return ["pod1", "pod2"]

    def get_logs(self, body):
        if body['namespace'] == "namespace1" and body['pod_name'] == "pod1":
            return "2021-12-02 10:54:04 test[1] INFO Test logs"
        else:
            raise LogsNotFoundE(body['namespace'], body['pod_name'])
