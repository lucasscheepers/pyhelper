from .utils import start_bot  # noqa, only imported so that the bot is started
from .utils import MAIN_BOT_ID, OFF_TOPIC_ID, RESPONSE_TIMEOUT, TEAM_ID
from .utils import driver as driver_fixture
from .utils import expect_reply

# Hacky workaround to import the fixture without linting errors
driver = driver_fixture


def test_start(driver):
    post = driver.create_post(OFF_TOPIC_ID, "starting integration tests!")
    assert expect_reply(driver, post)["message"] == "Bring it on!"
