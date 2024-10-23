import os

import allure
import pytest
from playwright.sync_api import Page, expect

from pages.page_manager import PageManager
from rift.rift_processor import rift_ai


@allure.title("Swag Labs Login Using AI")
@allure.description("This test attempts to login using valid credentials")
@allure.tag("UI", "POSITIVE")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.webtest
def test_login_users(page: Page, pm: PageManager) -> None:

    rift_ai('open https://www.saucedemo.com', page)
    rift_ai("enter 'standard_user' into username input", page)
    rift_ai("type 'secret_sauce' into password input", page)
    rift_ai("click on the login input", page)

    rift_ai(f"verify the page title is 'Swag Labs'", page)
    rift_ai(f"assert the url contains '{os.getenv('BASE_URL')}/inventory.html'", page)

    png_bytes = page.screenshot()
    allure.attach(
        png_bytes,
        name="User has logged in successfully.",
        attachment_type=allure.attachment_type.PNG
    )
