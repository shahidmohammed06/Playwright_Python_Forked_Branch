from playwright.sync_api import Page

from pages.cart import CartPage
from pages.checkout_step import CheckoutStepPage
from pages.inventory import InventoryPage
from pages.login import LoginPage


class PageManager:

    def __init__(self, page: Page):

        self.login_page = LoginPage(page)
        self.inventory_page = InventoryPage(page)
        self.cart_page = CartPage(page)
        self.checkout_step_page = CheckoutStepPage(page)

