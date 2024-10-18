import os

from playwright.sync_api import Page
from cryptography.fernet import Fernet

# Load the key and encrypted password
with open("secret.key", "rb") as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)

with open("password.enc", "rb") as password_file:
    encrypted_password = password_file.read()

# Decrypt the password
decrypted_password = cipher_suite.decrypt(encrypted_password).decode()

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
        self.username_input.fill(username)
        self.username_input.fill(decrypted_password);
        self.login_button.click()
