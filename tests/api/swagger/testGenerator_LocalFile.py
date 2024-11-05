
#swagger_spec = load_swagger_from_file(f"{project_root}/data/swagger_file.json")

from pathlib import Path
import yaml
import requests
from openapi_spec_validator import validate_spec
from utils.getProjectRoot import find_project_root


current_file_path = Path(__file__).resolve()
project_root = find_project_root(current_file_path, 'requirements.txt')
# Load the Swagger file
with open(f"{project_root}/data/swagger_file.json", 'r') as file:
    swagger_spec = yaml.safe_load(file)

# Validate the spec
validate_spec(swagger_spec)

# Base URL for the API
base_url = "https://petstore.swagger.io/v2/"  # Replace with the API's base URL

# Iterate over each path and method
for path, methods in swagger_spec['paths'].items():
    for method, details in methods.items():
        url = f"{base_url}{path}"
        print(f"Generating test for {method.upper()} {url}")

        # Gather parameters
        params = {}
        headers = {}

        for param in details.get('parameters', []):
            if param['in'] == 'query':
                params[param['name']] = "test"
            elif param['in'] == 'header':
                headers[param['name']] = "test"

        # Send requests and validate response
        response = requests.request(method, url, params=params, headers=headers)

        # Print results for demonstration
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")
