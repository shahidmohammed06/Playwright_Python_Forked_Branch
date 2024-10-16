import os
from typing import Generator

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, Playwright, APIRequestContext

from pages.page_manager import PageManager


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="qa", help="Environment to run tests against: qa, stage, prod"
    )


@pytest.fixture(scope="session", autouse=True)
def load_env(pytestconfig):
    env = pytestconfig.getoption("env")
    env_file = f".env.{env}"
    load_dotenv(dotenv_path=env_file)
    print(f"Loaded environment: {env}")


@pytest.fixture
def pm(page: Page) -> PageManager:
    return PageManager(page)


@pytest.fixture(scope="session")
def api_request(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(
        base_url=os.getenv('API_URL')
    )
    yield request_context
    request_context.dispose()
