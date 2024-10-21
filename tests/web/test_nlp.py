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

    rift_ai('Navigate to https://www.saucedemo.com', page)
    rift_ai("Enter 'standard_user' into Username input", page)
    rift_ai("Enter 'secret_sauce' into Password input", page)
    rift_ai("Click on the Login button", page)

    # Verify that the user is navigated to the inventory page
    expect(page).to_have_url(f"{os.getenv('BASE_URL')}/inventory.html")


    png_bytes = page.screenshot()
    allure.attach(
        png_bytes,
        name="User has logged in successfully.",
        attachment_type=allure.attachment_type.PNG
    )
