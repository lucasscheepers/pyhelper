class LogsNotFoundE(Exception):
    """Raised when the namespace or pod is not found

    Attributes:
    namespace -- the name of the namespace
    pod name -- the name of the pod
    """
    def __init__(self, namespace, pod_name, message=""):
        self.namespace = namespace
        self.pod_name = pod_name
        self.message = message.join(f"The logs of the pod '{pod_name}' was not found in the namespace '{namespace}'")
        super().__init__(self.message)
