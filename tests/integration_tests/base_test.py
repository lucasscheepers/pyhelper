from .utils import OFF_TOPIC_ID
from .utils import driver as driver_fixture
from .utils import expect_reply

driver = driver_fixture


class TestBasePlugin:
    def test_help(self, driver):
        post = driver.create_post(OFF_TOPIC_ID, "help")
        reply = expect_reply(driver, post)

        assert reply["message"] == (
            "| COMMANDS | INFORMATION | MANDATORY ARGUMENTS | OPTIONAL ARGUMENTS\n"
            "| :-: | :-: | :-: | :-: |\n"
            "| help | *Retrieve a list of all the commands & arguments including further explanation* | *None* "
            "| *None* |\n"
            "| git create | *Create new merge requests, roll out new releases or open new issues* "
            "| merge-request **or** release **or** issue **or** -h *= help* | *None* |\n"
            "| git close | *Close issues* | issue **or** -h *= help* | *None* |\n"
            "| kubectl get | *Retrieve a list of the namespaces or running applications in the Kubernetes cluster or "
            "logs of a specific application* | namespaces **or** pods **or** logs **or** -h *= help* | *None* |\n"
        )
