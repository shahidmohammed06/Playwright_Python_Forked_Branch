from playwright.sync_api import Page

from pages.login import LoginPage


class PageManager:

    def __init__(self, page: Page):

        self.login_page = LoginPage(page)

