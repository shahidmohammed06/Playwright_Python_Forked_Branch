from http import HTTPStatus

import allure
import pytest
from swagger.generated-python-client

from utils.logger import logger


@pytest.fixture(scope="session")
def user_ids():
    ids = []
    yield ids

api_client = ApiClient()
my_api = Store_API(api_client)

@allure.title("Add new product in store")
@allure.description("This test attempts to add a new product in pet store")
@allure.tag("API", "CRUD", "POSITIVE")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.apitest
def test_create_user(api_request: APIRequestContext, user_ids) -> None:
    payload = {"id": 0,
               "petId": 0,
               "quantity": 0,
               "shipDate": "2024-11-04T10:54:36.704Z",
               "status": "placed",
               "complete": True
               }
    allure.attach(str(payload), "Request Body")
    response = api_request.post(url="/api/users", data=payload)
    assert response.ok

    json_response = response.json()
    allure.attach(str(json_response), "Response Body")
    logger.info("Create User API Response:\n{}".format(json_response))
    assert json_response["name"] == payload.get("name")
    user_ids.append(json_response["id"])
