import os

import allure
import pytest
from playwright.sync_api import Page, expect

from pages.page_manager import PageManager

test_data = [
    {"username": "standard_user", "password": "secret_sauce"},
    {"username": "problem_user", "password": "secret_sauce"},
    {"username": "error_user", "password": "secret_sauce"},
]


@allure.title("Swag Labs Login")
@allure.description("This test attempts to login using valid credentials")
@allure.tag("UI", "POSITIVE")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.webtest
@pytest.mark.parametrize("data", test_data)
def test_login_users(data, page: Page, pm: PageManager) -> None:
    # Navigate to the login page
    pm.login_page.navigate()

    # Verify the title and logo text
    expect(page).to_have_title('Swag Labs')
    expect(pm.login_page.login_logo).to_have_text('Swag Labs')

    # Perform login with valid credentials
    pm.login_page.login(data["username"], data["password"])

    # Attach a screenshot after login
    png_bytes = page.screenshot()
    allure.attach(
        png_bytes,
        name="User has logged in",
        attachment_type=allure.attachment_type.PNG
    )

    # Verify that the user is navigated to the inventory page
    expect(page).to_have_url(f"{os.getenv('BASE_URL')}/inventory.html")
