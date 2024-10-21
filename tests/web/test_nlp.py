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

    rift_ai('Open https://www.saucedemo.com', page)
    rift_ai("Type 'standard_user' into the Username input field", page)

    png_bytes = page.screenshot()
    allure.attach(
        png_bytes,
        name="Entered the username",
        attachment_type=allure.attachment_type.PNG
    )

    rift_ai("Type 'secret_sauce' into the Password input field", page)

    png_bytes = page.screenshot()
    allure.attach(
        png_bytes,
        name="Entered the username",
        attachment_type=allure.attachment_type.PNG
    )

    rift_ai("Click the Login button", page)

    # Verify that the user is navigated to the inventory page
    expect(page).to_have_url(f"{os.getenv('BASE_URL')}/inventory.html")
