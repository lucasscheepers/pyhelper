from .utils_integration import OFF_TOPIC_ID
from .utils_integration import driver as driver_fixture
from .utils_integration import expect_reply

driver = driver_fixture


class TestGitLabPlugin:
    def test_help_git_create(self, driver):
        post = driver.create_post(OFF_TOPIC_ID, "git create -h")
        reply = expect_reply(driver, post)

        assert reply["message"] == (
            "| COMMANDS | INFORMATION | MANDATORY ARGUMENTS | OPTIONAL ARGUMENTS\n"
            "| :-: | :-: | :-: | :-: |\n"
            "| **NOTE: ALL MANDATORY & OPTIONAL ARGUMENTS WITH IDENTIFIER ARE LIMITED TO ONE WORD, "
            "EXCEPT FOR THE ARGUMENTS IN <ANGLE BRACKETS>** |\n"
            "| merge-request | *Create a new merge request* | -pn, --project_name *= the name of the specific project* "
            "**and** -sb, --source_branch *= the branch to be merged* | -tb, --target_branch "
            "*= the branch it will be merged into. Default=master* **or** -ti, --title "
            "*= the title of the merge request. Default=UUID string* |\n"
            "| release | *Roll out a new release* | -pn, --project_name *= the name of the specific project* **and** "
            "-tn, --tag_name  *= the tag name to be released* "
            "| -ti, --title *= the title of the release. Default=None*\n"
            "| issue <description> | *Open a new issue* | -pn, --project_name "
            "*= the name of the specific project* **and** -ti, --title *= the title of the issue* | *None*\n"
        )

    def test_git_create_merge_request(self, driver):
        post = driver.create_post(OFF_TOPIC_ID, "git create merge-request -pn testProjectName -sb testSourceBranch "
                                                "-ti testTitle")
        reply = expect_reply(driver, post)

        assert reply["message"] == (
            "Command sent to the GitLab service with the following arguments:\n"
            f"- project_name: testProjectName\n"
            f"- title: testTitle\n"
            f"- source_branch: testSourceBranch\n"
            f"- target_branch: master\n"
        )

        post = driver.create_post(OFF_TOPIC_ID, "git create merge-request -pn testProjectName -sb testSourceBranch "
                                                "-tb testTargetBranch -ti testTitle")
        reply = expect_reply(driver, post)

        assert reply["message"] == (
            "Command sent to the GitLab service with the following arguments:\n"
            f"- project_name: testProjectName\n"
            f"- title: testTitle\n"
            f"- source_branch: testSourceBranch\n"
            f"- target_branch: testTargetBranch\n"
        )

    def test_git_create_release(self, driver):
        post = driver.create_post(OFF_TOPIC_ID, "git create release -pn testProjectName -tn testTagName")
        reply = expect_reply(driver, post)

        assert reply["message"] == (
            "Command sent to the GitLab service with the following arguments:\n"
            f"- project_name: testProjectName\n"
            f"- title: None\n"
            f"- tag_name: testTagName\n"
        )

        post = driver.create_post(OFF_TOPIC_ID, "git create release -pn testProjectName -tn testTagName "
                                                "-ti testTitle")
        reply = expect_reply(driver, post)

        assert reply["message"] == (
            "Command sent to the GitLab service with the following arguments:\n"
            f"- project_name: testProjectName\n"
            f"- title: testTitle\n"
            f"- tag_name: testTagName\n"
        )

    def test_git_create_issue(self, driver):
        post = driver.create_post(OFF_TOPIC_ID, 'git create issue "test description" -pn testProjectName -ti testTitle')
        reply = expect_reply(driver, post)

        assert reply["message"] == (
            "Command sent to the GitLab service with the following arguments:\n"
            f"- project_name: testProjectName\n"
            f"- title: testTitle\n"
            f"- description: test description\n"
        )

    def test_help_git_close(self, driver):
        post = driver.create_post(OFF_TOPIC_ID, 'git close -h')
        reply = expect_reply(driver, post)

        assert reply["message"] == (
            "| COMMANDS | INFORMATION | MANDATORY ARGUMENTS | OPTIONAL ARGUMENTS\n"
            "| :-: | :-: | :-: | :-: |\n"
            "| **NOTE: ALL MANDATORY & OPTIONAL ARGUMENTS WITH IDENTIFIER ARE LIMITED TO ONE WORD**\n"
            "| issue | *Close a issue in the project* | -pn, --project_name *= the name of "
            "the specific project* **and** -ti, --title  *= the title of the issue* | *None* |\n"
        )

    def test_git_close_issue(self, driver):
        post = driver.create_post(OFF_TOPIC_ID, 'git close issue -pn testProjectName -ti testTitle')
        reply = expect_reply(driver, post)

        assert reply["message"] == (
            "Command sent to the GitLab service with the following arguments:\n"
            f"- project_name: testProjectName\n"
            f"- title: testTitle\n"
        )
