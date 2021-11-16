from kubernetes.client.rest import ApiException
from kubernetes import client
from kubernetes.config import load_config
from exceptions.logs_not_found_exceptions import LogsNotFound
import logging

log = logging.getLogger("services/kubernetes_service.py")


class KubernetesService:
    def __init__(self):
        super().__init__()
        load_config()

        self.api_instance = client.CoreV1Api()

    def get_namespaces(self):
        try:
            api_response = self.api_instance.list_namespace()
            dict_response = api_response.to_dict()

            namespaces = []
            for item in dict_response['items']:
                namespaces.append(item['metadata']['name'])

            log.info(f"Retrieved the namespaces: {namespaces}")
            return namespaces
        except ApiException as e:
            raise ApiException(e)

    def get_pods(self, body):
        try:
            api_response = self.api_instance.list_namespaced_pod(namespace=body['namespace'])
            dict_response = api_response.to_dict()
            pods = []
            for item in dict_response['items']:
                pods.append(item['metadata']['name'])

            log.info(f"Retrieved the pods: {pods}")
            return pods
        except ApiException as e:
            raise ApiException(e)

    def get_logs(self, body):
        try:
            api_response = self.api_instance.read_namespaced_pod_log(name=body['pod_name'], namespace=body['namespace'])
            tail_logs = api_response[len(api_response)-16000:]

            log.info(f"Retrieved the logs: {tail_logs}")
            return tail_logs
        except ApiException:
            raise LogsNotFound(body['namespace'], body['pod_name'])
