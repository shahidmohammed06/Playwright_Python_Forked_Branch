import os

import allure
import pytest
from faker import Faker
from playwright.sync_api import Page, expect

from pages.page_manager import PageManager


# Fixture for logging in the user before running the test
@pytest.fixture(scope='function')
def login_user(page: Page, pm: PageManager) -> None:
    """
    Fixture to perform login actions and set up the user session.
    """
    # Navigate to the login page
    pm.login_page.navigate()

    # Verify the page title and logo text to ensure the correct page has loaded
    expect(page).to_have_title('Swag Labs')
    expect(pm.login_page.login_logo).to_have_text('Swag Labs')

    # Perform login using valid credentials
    pm.login_page.login('standard_user', 'secret_sauce')

    # Take a screenshot after login and attach it to the Allure report
    png_bytes = page.screenshot()
    allure.attach(
        png_bytes,
        name="User has logged in",
        attachment_type=allure.attachment_type.PNG
    )

    # Verify that the user is navigated to the inventory page
    expect(page).to_have_url(f"{os.getenv('BASE_URL')}/inventory.html")


# Test case for performing checkout after adding an item to the cart
@allure.title("Test Data Generation")
@allure.description("This test attempts to login using valid credentials and complete a checkout process")
@allure.tag("UI", "POSITIVE")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.webtest
def test_data_generation(login_user, page: Page, pm: PageManager) -> None:
    # Add a backpack to the shopping cart from the inventory page
    pm.inventory_page.add_back_pack_to_cart()

    # Click on the shopping cart link to go to the cart
    pm.inventory_page.click_shopping_cart_link()

    # Click on the checkout button to proceed to the checkout process
    pm.cart_page.click_checkout()

    # Use Faker to generate random first name, last name, and postal code for the checkout form
    faker = Faker()
    pm.checkout_step_page.fill_checkout_step_one(faker.first_name(), faker.last_name(), faker.zipcode())

    # Take a screenshot after filling the checkout step 1 form and attach it to the Allure report
    png_bytes = page.screenshot()
    allure.attach(
        png_bytes,
        name="User has filled the checkout step 1",
        attachment_type=allure.attachment_type.PNG
    )

    # Click 'Continue' to proceed to the next step of checkout
    pm.checkout_step_page.click_continue()

    # Click 'Finish' to complete the order
    pm.checkout_step_page.click_finish()

    # Validate that the order completion message is displayed
    expect(pm.checkout_step_page.complete_header_text).to_have_text('Thank you for your order!')

    # Take a screenshot after completing the checkout and attach it to the Allure report
    png_bytes = page.screenshot()
    allure.attach(
        png_bytes,
        name="User has completed the checkout",
        attachment_type=allure.attachment_type.PNG
    )
