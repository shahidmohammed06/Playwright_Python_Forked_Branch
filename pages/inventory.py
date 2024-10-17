from playwright.sync_api import Page


class InventoryPage:

    def __init__(self, page: Page):
        self.page = page
        self.add_to_cart_back_pack_button = page.locator('#add-to-cart-sauce-labs-backpack')
        self.shopping_cart_container_link = page.locator('#shopping_cart_container')

    def add_back_pack_to_cart(self):
        self.add_to_cart_back_pack_button.click()

    def click_shopping_cart_link(self):
        self.shopping_cart_container_link.click()