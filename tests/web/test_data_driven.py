import os

import allure
import openpyxl
import pytest
from playwright.sync_api import Page, expect

from pages.page_manager import PageManager


def read_excel(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header row
        data.append({
            "username": row[0],
            "password": row[1],
        })
    return data


@allure.title("Data Driven Test")
@allure.description("This test attempts to login using data reading from excel")
@allure.tag("UI", "POSITIVE")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.webtest
@pytest.mark.parametrize("data", read_excel("data/test_data.xlsx"))
def test_login(data, page: Page, pm: PageManager):
    # Navigate to the login page
    pm.login_page.navigate()

    # Verify the title and logo text
    expect(page).to_have_title('Swag Labs')
    expect(pm.login_page.login_logo).to_have_text('Swag Labs')

    # Perform login with valid credentials
    pm.login_page.login(data["username"], data["password"])

    # Verify that the user is navigated to the inventory page
    expect(page).to_have_url(f"{os.getenv('BASE_URL')}/inventory.html")