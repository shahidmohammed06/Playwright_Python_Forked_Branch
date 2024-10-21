from bs4 import BeautifulSoup
from playwright.sync_api import Page


def find_locator(page: Page, element_type: str, text: str):
    page_source = page.content()

    soup = BeautifulSoup(page_source, 'html.parser')

    for element in soup.find_all(element_type):

        element_id = element.get('id')
        element_name = element.get('name')
        element_class = element.get('class')
        element_type = element.get('type')
        element_placeholder = str(element.get('placeholder'))
        element_text = element.getText()

        print(f"element_id is {element_id}")
        print(f"element_name is {element_name}")
        print(f"element_class is {element_class}")
        print(f"element_placeholder is {element_placeholder}")

        text = text.lower()

        if text in element_id:
            return page.locator(f"[id='{element_id}']")

        elif text in element_name:
            return page.locator(f"[name='{element_name}']")

        elif text in element_class:
            return page.locator(f".{element_class}")

        elif text in element_type:
            return page.locator(f"[type='{element_type}']")

        elif text in element_placeholder.lower():
            return page.get_by_placeholder(element_placeholder)

        elif text in element_text:
            return page.get_by_text(element_text)

    return None
