from bs4 import BeautifulSoup
from playwright.sync_api import Page


def find_locator(page: Page, element_type: str, text: str):
    page_source = page.content()

    soup = BeautifulSoup(page_source, 'html.parser')

    # Convert the text to lowercase for case-insensitive comparison
    text = text.lower()

    # Search for the first matching element
    element = soup.find(lambda tag: tag.name == element_type and (
            text in (tag.get('id', '').lower()) or
            text in (tag.get('name', '').lower()) or
            text in ' '.join(tag.get('class', [])).lower() or
            text in (tag.get('type', '').lower()) or
            text in (tag.get('placeholder', '').lower()) or
            text in tag.get_text().strip().lower()
    ))

    # If no element is found, try again without the tag.name check
    if not element:
        possible_elements = soup.find(lambda tag: (
                text in (tag.get('id', '').lower()) or
                text in (tag.get('name', '').lower()) or
                text in ' '.join(tag.get('class', [])).lower() or
                text in (tag.get('type', '').lower()) or
                text in (tag.get('placeholder', '').lower()) or
                text in tag.get_text().strip().lower()
        ))

        if len(possible_elements) > 1:
            raise MultipleElementsFoundException(possible_elements,
                                                 f"Multiple elements found for '{text}'. Found: {len(possible_elements)} elements.")
        elif len(possible_elements) == 1:
            element = possible_elements
        else:
            raise ElementNotFoundException(f"Element with '{text}' not found in type '{element_type}'.")

    if element:
        element_id = element.get('id', '')
        element_name = element.get('name', '')
        element_class = ' '.join(element.get('class', [])).strip()
        element_type_attr = element.get('type', '')
        element_placeholder = element.get('placeholder', '')
        element_text = element.get_text().strip()

        print(f"element_id is {element_id}")
        print(f"element_name is {element_name}")
        print(f"element_class is {element_class}")
        print(f"element_placeholder is {element_placeholder}")

        # Return the correct locator based on which attribute matched the text
        if text in element_id.lower():
            return page.locator(f"[id='{element_id}']")
        elif text in element_name.lower():
            return page.locator(f"[name='{element_name}']")
        elif text in element_class.lower():
            return page.locator(f".{element_class.replace(' ', '.')}")
        elif text in element_type_attr.lower():
            return page.locator(f"[type='{element_type_attr}']")
        elif text in element_placeholder.lower():
            return page.get_by_placeholder(element_placeholder)
        elif text in element_text.lower():
            return page.get_by_text(element_text)

    raise ElementNotFoundException(f"Element with '{text}' not found in type '{element_type}'.")


class ElementNotFoundException(Exception):

    def __init__(self, message):
        super().__init__(message)

class MultipleElementsFoundException(Exception):
    """Custom exception raised when multiple elements are found."""
    def __init__(self, elements, message="Multiple elements found:"):
        self.elements = elements
        self.message = message
        super().__init__(self.format_message())

    def format_message(self):
        # Format the message to include all found elements
        elements_details = '\n'.join([str(element) for element in self.elements])
        return f"{self.message}\n{elements_details}"
