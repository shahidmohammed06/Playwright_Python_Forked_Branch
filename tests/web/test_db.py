# Fixture for setting up a DB connection
import allure
import pytest
from playwright.sync_api import Page

from db.connection import connect_to_db
from utils.logger import logger


@pytest.fixture(scope='function')
def db_connection():
    connection = connect_to_db()
    logger.info('db connection has been established.')
    yield connection
    connection.close()
    logger.info('db connection has been closed.')


@allure.title("DB Validation Test")
@allure.description("This test attempts to validate db entries")
@allure.tag("UI", "DB", "POSITIVE")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.webtest
@pytest.mark.skip('DB setup is pending')
def test_db_users(page: Page, db_connection) -> None:
    with db_connection.cursor() as cursor:
        # Query the database to check if the item was added to the user's cart
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()

    assert result is not None, "Item was not found in the database"

    # Check that there are exactly 3 users in the result
    assert len(result) == 3, 'User count is not matching'

    # Check the name of the first user in the result
    first_user = result[0]  # Access the first row
    assert first_user['name'] == 'Alice', 'First user\'s name does not match'
    assert first_user['email'] == 'alice@example.com', 'First user\'s email does not match'
