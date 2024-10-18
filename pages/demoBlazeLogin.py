import os

from playwright.sync_api import Page
from utils.logger import logger

class DemoBlazeLoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator('#loginusername')
        self.password_input = page.locator('#loginpassword')
        self.login_button = page.locator('button', has_text='Log in')      
        self.headerLoginBtn = page.locator("#login2")

    def navigate(self):
        self.page.goto(os.getenv("DEMOBLAZE_URL"))

    def login(self, username: str, password: str):
        self.headerLoginBtn.click()
        logger.info("CLicked on login button")
        self.username_input.fill(username)
        logger.info("Entered userName")
        self.username_input.fill(decrypted_password)
        logger.info("Entered password")
        self.login_button.click()
        logger.info("Clicked on login button")
