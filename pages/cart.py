from playwright.sync_api import Page


class CartPage:

    def __init__(self, page: Page):
        self.page = page
        self.checkout_button = page.locator('#checkout')

    def click_checkout(self):
        self.checkout_button.click()