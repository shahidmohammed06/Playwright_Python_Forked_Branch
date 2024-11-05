## For generating swagger client Install OpenAPI Generator via npm
 >>npm install @openapitools/openapi-generator-cli -g

## For Generating Python Client Code Using OpenAPI Generator
 >> openapi-generator-cli generate -i path/to/swagger.yaml -g python -o ./generated-python-client
 
## Install the generated python client, move to generated-python-client folder
>> pip install -e .

## Example usage of generated python client :unit test
import unittest
from my_generated_client import ApiClient, MyApi, MyRequestBodyModel

class TestMyApi(unittest.TestCase):
    def setUp(self):
        # Initialize the API client and the specific API
        self.api_client = ApiClient()
        self.api = MyApi(self.api_client)

    def test_some_endpoint(self):
        # Create a sample request body (replace with actual structure if needed)
        request_body = MyRequestBodyModel(key1="value1", key2="value2")
        
        # Call the API method
        response = self.api.some_endpoint(request_body)
        
        # Assertions to validate the response
        self.assertIsNotNone(response, "Response should not be None")
        self.assertEqual(response.status_code, 200, "Status code should be 200")  # Check status code
        
        # Additional assertions based on response content
        self.assertTrue(hasattr(response, 'key'), "Response should have 'key' attribute")
        self.assertEqual(response.key, "expected_value", "Key should match the expected value")
        self.assertTrue(response.success, "Response success flag should be True")
        
        # Example for checking a list in the response
        self.assertIsInstance(response.data, list, "Response data should be a list")
        self.assertGreater(len(response.data), 0, "Data list should not be empty")
        
        # Checking specific values within response data if applicable
        first_item = response.data[0]
        self.assertEqual(first_item['name'], "expected_name", "First item's name should match expected value")

if __name__ == "__main__":
    unittest.main()


## Explanation of Assertions Used
assertIsNotNone(response, "Response should not be None")
Ensures the API response isn’t None.

assertEqual(response.status_code, 200, "Status code should be 200")
Verifies that the HTTP status code is 200 (OK), which is typically expected for successful requests.

assertTrue(hasattr(response, 'key'), "Response should have 'key' attribute")
Checks that the response object contains a specific attribute (key in this case).

assertEqual(response.key, "expected_value", "Key should match the expected value")
Verifies that a specific attribute (key) in the response matches the expected value.

assertTrue(response.success, "Response success flag should be True")
Ensures a success flag or similar indicator is set to True in the response.

assertIsInstance(response.data, list, "Response data should be a list")
Confirms that response.data is a list, if the response is expected to include one.

assertGreater(len(response.data), 0, "Data list should not be empty")
Ensures that the list in response.data has at least one item.

assertEqual(first_item['name'], "expected_name", "First item's name should match expected value")

## can be converted to pytest as below
>> import pytest
from my_generated_client import ApiClient, MyApi, MyRequestBodyModel

# Define a fixture for setting up the API client and API instance
@pytest.fixture
def api_client():
    client = ApiClient()
    api = MyApi(client)
    return api

# Test function that uses the fixture
def test_some_endpoint(api_client):
    # Create a sample request body
    request_body = MyRequestBodyModel(key1="value1", key2="value2")
    
    # Call the API method
    response = api_client.some_endpoint(request_body)
    
    # Assertions to validate the response
    assert response is not None, "Response should not be None"
    assert response.status_code == 200, "Status code should be 200"  # Check status code
    
    # Additional assertions based on response content
    assert hasattr(response, 'key'), "Response should have 'key' attribute"
    assert response.key == "expected_value", "Key should match the expected value"
    assert response.success is True, "Response success flag should be True"
    
    # Example for checking a list in the response
    assert isinstance(response.data, list), "Response data should be a list"
    assert len(response.data) > 0, "Data list should not be empty"
    
    # Checking specific values within response data if applicable
    first_item = response.data[0]
    assert first_item['name'] == "expected_name", "First item's name should match expected value"

###########################################


## Running Tests in Generated Python Client

>> python -m unittest discover generated-python-client/test
