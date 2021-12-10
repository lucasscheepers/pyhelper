import os
from unittest import mock
from tests.unit_tests import utils
from services.kubernetes_service import KubernetesService
from exceptions.logs_not_found_exception import LogsNotFoundE
import pytest
from kubernetes.client.rest import ApiException


class TestKubernetesService:
    @mock.patch.dict(os.environ, {"DISABLE_KUBERNETES_CONFIG": "True"})
    def test_get_namespaces(self):
        self.service = KubernetesService()

        with mock.patch.object(self.service.api_instance, 'list_namespace',
                               return_value=utils.kubernetes_namespaces_response()):
            actual_result = self.service.get_namespaces()
            assert actual_result == ['default', 'kube-node-lease', 'kube-public', 'kube-system']

    @mock.patch.dict(os.environ, {"DISABLE_KUBERNETES_CONFIG": "True"})
    def test_get_namespaces_exception(self):
        self.service = KubernetesService()

        with mock.patch.object(self.service.api_instance, 'list_namespace',
                               side_effect=ApiException):

            with pytest.raises(ApiException):
                self.service.get_namespaces()

    @mock.patch.dict(os.environ, {"DISABLE_KUBERNETES_CONFIG": "True"})
    def test_get_pods(self):
        self.service = KubernetesService()

        with mock.patch.object(self.service.api_instance, 'list_namespaced_pod',
                               return_value=utils.kubernetes_pods_response()):

            body = {
                'event_type': 'get_pods',
                'namespace': 'kube-system',
            }

            actual_result = self.service.get_pods(body)
            assert actual_result == ['mm-demo', 'rabbitmq-server-0']

    @mock.patch.dict(os.environ, {"DISABLE_KUBERNETES_CONFIG": "True"})
    def test_get_pods_exception(self):
        self.service = KubernetesService()

        with mock.patch.object(self.service.api_instance, 'list_namespaced_pod',
                               side_effect=ApiException):

            body = {
                'event_type': 'get_pods',
                'namespace': 'unkown-namespace',
            }

            with pytest.raises(ApiException):
                self.service.get_pods(body)

    @mock.patch.dict(os.environ, {"DISABLE_KUBERNETES_CONFIG": "True"})
    def test_get_logs(self):
        self.service = KubernetesService()

        with mock.patch.object(self.service.api_instance, 'read_namespaced_pod_log',
                               return_value=utils.kubernetes_logs_respnose()):

            body = {
                'event_type': 'get_logs',
                'namespace': 'kube-system',
                'pod_name': 'sonar-0'
            }

            actual_result = self.service.get_logs(body)
            assert actual_result == "11:56:11.571 DEBUG: Using pattern 'cov/coverage.xml' to find reports " \
                                    "11:56:11.687 INFO: Python test coverage " \
                                    "11:56:11.689 INFO: Parsing report " \
                                    "'/Users/lucasscheepers/Desktop/Lucas/School/Semester 8 - Stage IND/3. " \
                                    "Implementation/ChatOps bot/cov/coverage.xml' " \
                                    "11:56:11.750 INFO: Sensor Cobertura Sensor for Python coverage " \
                                    "[python] (done) | time=180ms" \
                                    "11:56:11.750 INFO: Sensor PythonXUnitSensor [python]"

    @mock.patch.dict(os.environ, {"DISABLE_KUBERNETES_CONFIG": "True"})
    def test_get_logs_exception(self):
        self.service = KubernetesService()

        with mock.patch.object(self.service.api_instance, 'read_namespaced_pod_log',
                               side_effect=ApiException):

            body = {
                'event_type': 'get_logs',
                'namespace': 'kube-system',
                'pod_name': 'unknown-pod'
            }

            with pytest.raises(LogsNotFoundE):
                self.service.get_logs(body)
