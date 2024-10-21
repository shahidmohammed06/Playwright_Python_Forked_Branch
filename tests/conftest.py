import os
from typing import Generator

import openpyxl
import pytest
from dotenv import load_dotenv
from openpyxl import Workbook
from playwright.sync_api import Page, Playwright, APIRequestContext

from pages.page_manager import PageManager


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="qa", help="Environment to run tests against: qa, stage, prod"
    )


@pytest.fixture(scope="session", autouse=True)
def load_env(pytestconfig):
    env = pytestconfig.getoption("env")
    env_file = f".env.{env}"
    load_dotenv(dotenv_path=env_file)
    print(f"Loaded environment: {env}")


@pytest.fixture
def pm(page: Page) -> PageManager:
    return PageManager(page)


@pytest.fixture(scope="session")
def api_request(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(
        base_url=os.getenv('API_URL')
    )
    yield request_context
    request_context.dispose()

# Store test results during execution
test_results = []

# Create Excel report in the "test-results" folder
def create_excel_report(filename="test_report.xlsx"):
    # Create the 'test-results' folder if it doesn't exist
    results_dir = "test-results"

    try:
        # Check if the directory exists; if not, create it
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
    except FileExistsError:
        pass

    file_path = os.path.join(results_dir, filename)

    if not os.path.exists(file_path):
        wb = Workbook()
        ws = wb.active
        ws.title = "Test Report"
        # Add headers to the report
        headers = ["Test Name", "Outcome", "Duration (s)", "Error Message"]
        ws.append(headers)
        wb.save(file_path)

    return file_path


# Hook to log test results during execution
@pytest.hookimpl(trylast=True)
def pytest_runtest_logreport(report):

    if report.when == "call":

        test_name = report.nodeid.split("[")[0]
        outcome = report.outcome
        duration = report.duration
        error_msg = str(report.longrepr) if report.failed else ""

        # Collect the result
        test_results.append([test_name, outcome, duration, error_msg])


# Hook to create the report at the end of test execution
@pytest.hookimpl(trylast=True)
def pytest_terminal_summary(terminalreporter):

    # Load or create the Excel file after tests are done
    report_file = create_excel_report()

    # Open the workbook and select the active worksheet
    wb = openpyxl.load_workbook(report_file)
    ws = wb.active

    # Write the collected test results to the worksheet
    for result in test_results:
        ws.append(result)

    # Auto-size the columns
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    # Save the workbook after all tests
    if os.getenv('CI'):

        wb.save(report_file)
        # Print the location of the test results file
        print(f"\nTest results have been written to {report_file}\n")