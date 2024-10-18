from http import HTTPStatus

import allure
import pytest
from playwright.sync_api import APIRequestContext

from utils.logger import logger


@pytest.fixture(scope="session")
def user_ids():
    ids = []
    yield ids


@allure.title("Create new user")
@allure.description("This test attempts to create a new user using reqres.in API")
@allure.tag("API", "CRUD", "POSITIVE")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.apitest
def test_create_user(api_request: APIRequestContext, user_ids) -> None:
    payload = {
        "name": "John Doe",
        "job": "QA Automation Engineer"
    }
    allure.attach(str(payload), "Request Body")
    response = api_request.post(url="/api/users", data=payload)
    assert response.ok

    json_response = response.json()
    allure.attach(str(json_response), "Response Body")
    logger.info("Create User API Response:\n{}".format(json_response))
    assert json_response["name"] == payload.get("name")
    user_ids.append(json_response["id"])


@allure.title("Check for non-existing user")
@allure.description("This test attempts to get a non-existing user using reqres.in API")
@allure.tag("API", "CRUD", "NEGATIVE")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.apitest
def test_get_user_not_found(api_request: APIRequestContext, user_ids) -> None:
    response = api_request.get(url="/api/users/0")
    assert response.status == HTTPStatus.NOT_FOUND.value
    json_response = response.json()
    allure.attach(str(json_response), "Response Body")
    logger.info("Get User API Response - User Not Found:\n{}".format(json_response))


@allure.title("Check for existing user")
@allure.description("This test attempts to get an existing user using reqres.in API")
@allure.tag("API", "CRUD", "POSITIVE")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.apitest
def test_get_user_happy_flow(api_request: APIRequestContext) -> None:
    response = api_request.get(url="/api/users/2")
    assert response.status == HTTPStatus.OK.value

    json_response = response.json()
    allure.attach(str(json_response), "Response Body")
    logger.info("Get User API Response - Happy Flow:\n{}".format(json_response))
    assert json_response["data"]["id"] == 2
