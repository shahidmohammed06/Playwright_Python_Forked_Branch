import os

import allure
import pytest
from playwright.sync_api import Page, expect
from utils.logger import logger

from pages.page_manager import PageManager
from cryptography.fernet import Fernet

# Load the key and encrypted password
with open("secret.key", "rb") as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)

with open("password.enc", "rb") as password_file:
    encrypted_password = password_file.read()

# Decrypt the password
decrypted_password = cipher_suite.decrypt(encrypted_password).decode()

test_data = [
     {"username": "Test_Cuser5", "password": decrypted_password}
]

@allure.title("DemoBlaze Login")
@allure.description("This test attempts to login using valid credentials")
@allure.tag("UI", "POSITIVE")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.webtest
@pytest.mark.parametrize("data", test_data)
def test_demoBlazeLogin(data, page: Page, pm: PageManager) -> None:
    # Navigate to the login page
    pm.demoBlazeLoginPage.navigate()
    logger.info("Navigating to site: "+os.envgetenv('DEMOBLAZE_URL'))

    # Verify the title and logo text
    expect(page).to_have_title('STORE')

    # Perform login with valid credentials
    pm.demoBlazeLoginPage.login(data["username"], data["password"])

    # Attach a screenshot after login
    png_bytes = page.screenshot()
    allure.attach(
        png_bytes,
        name="User has logged in",
        attachment_type=allure.attachment_type.PNG
    )

    # Verify that the user is navigated to the inventory page
    expect(page).to_have_url(f"{os.getenv('DEMOBLAZE_URL')}")
