import logging
import click
from mmpy_bot import Plugin, listen_to
from mmpy_bot import Message
import plugins.base
from messaging.gitlab_rabbitmq_producer import GitLabRabbitMqProducer
import uuid

log = logging.getLogger("plugins/gitlab.py")


class GitLab(Plugin):
    def __init__(self):
        super().__init__()
        self.gitlab_rabbitmq_producer = GitLabRabbitMqProducer()

    @listen_to("git create -h")
    def help_git_create(self, message: Message):
        """Retrieves a list of all 'git create' commands & arguments including further explanation"""
        response = (
            "| COMMANDS | INFORMATION | MANDATORY ARGUMENTS | OPTIONAL ARGUMENTS\n"
            "| :-: | :-: | :-: | :-: |\n"
            "| mr | *Create a new merge request* | -pn, --project_name *= the name of the specific project* **and** "
            "-sb, --source_branch  *= the branch to be merged* "
            "| -tb, --target_branch *= the branch it will be merged into. Default=master* **or** -ti, --title *= "
            "the title of the merge request. Default=UUID string* |\n"
            "| r | *Roll out a new release* | -pn, --project_name *= the name of the specific project* **and** "
            "-tn, --tag_name  *= the tag name to be released* "
            "| -ti, --title *= the title of the release. Default=None*\n"
        )

        self.driver.reply_to(message, response)
        log.info(f"Sent successfully a response back to Mattermost")

    @listen_to("git create mr")
    @click.command(help="Creates a new merge request in a Git project")
    @click.option("-pn", "--project_name", type=str, help="The name of the project")
    @click.option("-ti", "--title", type=str, default=f"{uuid.uuid4()}", help="The title of the MR")
    @click.option("-sb", "--source_branch", type=str, help="The branch to be merged")
    @click.option("-tb", "--target_branch", type=str, default="master", help="The branch it will be merged into")
    def git_create_mr(
            self, message: Message, project_name: str, title: str, source_branch: str, target_branch: str
    ):
        """Creates a new merge request in a Git project."""
        try:
            body = {
                'event_type': 'create_mr',
                'project_name': project_name,
                'title': title,
                'source_branch': source_branch,
                'target_branch': target_branch
            }
            self.gitlab_rabbitmq_producer.produce_gitlab_data(body)

            response = (
                "Command sent to the GitLab service with the following arguments:\n"
                f"- project_name: {project_name}\n"
                f"- title: {title}\n"
                f"- source_branch: {source_branch}\n"
                f"- target_branch: {target_branch}\n"
            )

            self.driver.reply_to(message, response)
            log.info(f"Sent successfully a response back to Mattermost")
        except Exception as e:
            self.driver.reply_to(message, plugins.base.error_response(str(e)))
            log.error(f"An error has occured: {str(e)}")

    @listen_to("git create r")
    @click.command(help="Rolls out a new release of the project")
    @click.option("-pn", "--project_name", type=str, help="The name of the project")
    @click.option("-ti", "--title", type=str, default=None, help="The title of the release")
    @click.option("-tn", "--tag_name", type=str, help="The tag name to be released")
    def git_create_r(
            self, message: Message, project_name: str, title: str, tag_name: str
    ):
        """Rolls out a new release of the project"""
        try:
            body = {
                'event_type': 'create_r',
                'project_name': project_name,
                'title': title,
                'tag_name': tag_name,
            }
            self.gitlab_rabbitmq_producer.produce_gitlab_data(body)

            response = (
                "Command sent to the GitLab service with the following arguments:\n"
                f"- project_name: {project_name}\n"
                f"- title: {title}\n"
                f"- source_branch: {tag_name}\n"
            )

            self.driver.reply_to(message, response)
            log.info(f"Sent successfully a response back to Mattermost")
        except Exception as e:
            self.driver.reply_to(message, plugins.base.error_response(str(e)))
            log.error(f"An error has occured: {str(e)}")
