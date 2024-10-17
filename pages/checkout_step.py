from playwright.sync_api import Page


class CheckoutStepPage:

    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.locator('#first-name')
        self.last_name_input = page.locator('#last-name')
        self.postal_code_input = page.locator('#postal-code')
        self.continue_button = page.locator('#continue')
        self.finish_button = page.locator('#finish')
        self.complete_header_text = page.locator('[data-test="complete-header"]')

    def fill_checkout_step_one(self, first_name: str, last_name: str, zip_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(zip_code)

    def click_continue(self):
        self.continue_button.click()

    def click_finish(self):
        self.finish_button.click()
