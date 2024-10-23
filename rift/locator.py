from bs4 import BeautifulSoup, Tag
from playwright.sync_api import Page

attributes = ['id', 'name', 'class', 'type', 'placeholder', 'value']


def find_locator(page: Page, element_type: str, text: str, value=''):
    page_source = page.content()

    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all elements that match the specified type
    elements = soup.find_all(lambda tag: tag.name == element_type)

    element: Tag = None

    # If there are matching elements, find the one with the exact match first
    exact_match_found = False
    for el in elements:
        if count_matching_attributes(el, text) == 1:  # Check for exact matches
            element = el
            exact_match_found = True
            break

    # If no exact match is found, check for attribute counts
    if not exact_match_found:
        # Sort elements by the number of matching attributes (highest first)
        element = max(elements, key=lambda elm: count_matching_attributes(elm, text), default=None)

    if not element and value not in ('', None):

        for el in elements:
            if count_matching_attributes(el, value) == 1:  # Check for exact matches
                element = el
                exact_match_found = True
                break

        # If no exact match is found, check for attribute counts
        if not exact_match_found:
            # Sort elements by the number of matching attributes (highest first)
            element = max(elements, key=lambda elm: count_matching_attributes(elm, value), default=None)

    # If no element is found, try again without the tag.name check
    if not element:
        possible_elements = soup.find_all(lambda tag: (
                text.lower() in (tag.get('id', '').lower()) or
                text.lower() in (tag.get('name', '').lower()) or
                text.lower() in ' '.join(tag.get('class', [])).lower() or
                text.lower() in (tag.get('type', '').lower()) or
                text.lower() in (tag.get('placeholder', '').lower()) or
                text.lower() in tag.get_text().strip().lower()
        ))

        if len(possible_elements) > 1:
            raise MultipleElementsFoundException(possible_elements,
                                                 f"Multiple elements found for '{text}'. Found: {len(possible_elements)} elements.")
        elif len(possible_elements) == 1:
            element = possible_elements[0]
        else:
            raise ElementNotFoundException(f"Element with '{text}' not found in type '{element_type}'.")

    if element:
        return get_locator_for_element(page, element, text)

    raise ElementNotFoundException(f"Element with '{text}' not found in type '{element_type}'.")


def count_matching_attributes(tag: Tag, text: str):
    # Check for exact matches first
    if strict_locator_match(tag, text) == 1:
        return 1

    # If no exact matches, proceed to count matches
    return soft_locator_match(tag, text)


def strict_locator_match(tag: Tag, text: str):
    # Check for exact matches first
    for attr in attributes:
        if attr in tag.attrs:
            if attr != 'class':
                # Check case-sensitive for other attributes
                if text == tag.get(attr, ''):
                    return 1  # Exact match found
            else:
                # Check case-sensitive for 'class' attribute
                if text == ' '.join(tag.get(attr, [])):
                    return 1  # Exact match found


def soft_locator_match(tag: Tag, text: str):
    match_count = 0

    for attr in attributes:
        if attr in tag.attrs:
            if attr != 'class':
                # Check case-insensitive for other attributes
                if text.lower() in tag.get(attr, '').lower():
                    match_count += 1
            else:
                # Check case-insensitive for 'class' attribute
                if text.lower() in ' '.join(tag.get(attr, [])).lower():
                    match_count += 1

    # Check the tag's inner text for case-insensitive match
    if text.lower() in tag.get_text().strip().lower():
        match_count += 1

    return match_count


def get_locator_for_element(page: Page, element: Tag, text: str):
    element_id = element.get('id', '').strip()
    element_name = element.get('name', '').strip()
    element_class = ' '.join(element.get('class', [])).strip()
    element_placeholder = element.get('placeholder', '').strip()
    element_text = element.get_text().strip()

    # Return the correct locator based on which attribute matched the text
    if element_id:
        return page.locator(f"[id='{element_id}']")
    elif element_name:
        return page.locator(f"[name='{element_name}']")
    elif element_placeholder:
        return page.get_by_placeholder(element_placeholder)
    elif element_text.lower() == text.lower():
        locator = page.get_by_text(text)
        count = locator.count()
        if count == 1:
            return locator


    # If none of the specified attributes are present, build a selector from all available attributes
    attrs = element.attrs
    selectors = []
    for attr, value in attrs.items():
        if isinstance(value, list):
            value = ' '.join(value)  # Join class names or any list attribute
        if value.strip():  # Check if the attribute value is not empty
            selectors.append(f"[{attr}='{value.strip()}']")

    # Join the selectors to form a combined locator
    if selectors:
        combined_selector = ''.join(selectors)
        return page.locator(combined_selector)

    # If no valid attribute or text is found, raise an error
    raise ValueError("No valid attributes or text found to generate a selector.")


class ElementNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)


class MultipleElementsFoundException(Exception):
    def __init__(self, elements, message="Multiple elements found:"):
        self.elements = elements
        self.message = message
        super().__init__(self.format_message())

    def format_message(self):
        elements_details = '\n'.join([str(element) for element in self.elements])
        return f"{self.message}\n{elements_details}"
