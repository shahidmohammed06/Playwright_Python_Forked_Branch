import allure
import pytest
from playwright.sync_api import expect, Page, Route

from pages.page_manager import PageManager


@allure.title("Mock API Request and Response")
@allure.description("This test attempts to mock the api request and response")
@allure.tag("UI", "API", "MOCK", "POSITIVE")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.webtest
def test_mock_api(page: Page, pm: PageManager) -> None:
    def handle(route: Route):
        json = [{"name": "Strawberry", "id": 21}]
        # fulfill the route with the mock data
        route.fulfill(json=json)

    # Intercept the route to the fruit API
    page.route("*/**/api/v1/fruits", handle)

    # Go to the page
    page.goto("https://demo.playwright.dev/api-mocking")

    # Assert that the Strawberry fruit is visible
    expect(page.get_by_text("Strawberry")).to_be_visible()


@allure.title("Mock API and Modify Response")
@allure.description("This test attempts to mock the api and modifies response")
@allure.tag("UI", "API", "MOCK", "POSITIVE")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.webtest
def test_mock_api_modify_response(page: Page) -> None:

    def handle(route: Route):
        response = route.fetch()
        json = response.json()
        json.append({"name": "Loquat", "id": 100})
        # Fulfill using the original response, while patching the response body
        # with the given JSON object.
        route.fulfill(response=response, json=json)

    page.route("https://demo.playwright.dev/api-mocking/api/v1/fruits", handle)

    # Go to the page
    page.goto("https://demo.playwright.dev/api-mocking")

    # Assert that the new fruit is visible
    expect(page.get_by_text("Loquat", exact=True)).to_be_visible()
