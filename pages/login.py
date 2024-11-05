import os

from playwright.sync_api import Page

from utils.logger import logger


class LoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator('#user-name')
        self.password_input = page.locator('#password')
        self.login_button = page.locator('#login-button')
        self.login_logo = page.locator('.login_logo')

    def navigate(self):
        logger.info(f"navigating to {os.getenv('BASE_URL')}")
        self.page.goto(os.getenv("BASE_URL"))
        logger.info(f"navigated to {os.getenv('BASE_URL')}")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
