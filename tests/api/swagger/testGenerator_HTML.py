from bs4 import BeautifulSoup
import requests
import json
import re


def load_swagger_from_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find script tag that contains JSON (customize if necessary)
        script = soup.find('script', string=re.compile(r'var\s+spec\s*=\s*({.*?});', re.DOTALL))

        if script:
            # Extract JSON content
            match = re.search(r'var\s+spec\s*=\s*({.*?});', script.string, re.DOTALL)
            if match:
                swagger_json = json.loads(match.group(1))
                return swagger_json

        print("Swagger JSON not found in HTML.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Swagger HTML: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


# Example usage
swagger_url = "https://demoqa.com/swagger/#"
swagger_spec = load_swagger_from_html(swagger_url)

if swagger_spec:
    print("Swagger spec loaded successfully.")
else:
    print("Failed to load Swagger spec.")
