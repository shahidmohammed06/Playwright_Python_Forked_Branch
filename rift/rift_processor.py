import spacy
from playwright.sync_api import Page
from spacy.matcher import Matcher

from rift.locator import find_locator

# Load the pre-trained spaCy model
nlp = spacy.load("en_core_web_sm")

# Create a matcher for recognizing commands
matcher = Matcher(nlp.vocab)

# Define patterns for Open, Type, Click, and Verify commands

# Open Command (e.g., "Open https://www.google.com")
open_pattern = [{"LOWER": "open"}, {"LIKE_URL": True}]
matcher.add("OPEN", [open_pattern])

# Type Command (e.g., 'Type "hello" into the search input field')
type_pattern = [
    {"LOWER": "type"},  # Match the word 'Type'
    {"IS_QUOTE": True, "OP": "?"},  # Optionally match an opening quote
    {"TEXT": {"REGEX": r"\w+"}, "OP": "+"},  # Match alphanumeric words with special characters (e.g., 'hello', 'secret_sauce')
    {"IS_QUOTE": True, "OP": "?"},  # Optionally match a closing quote
    {"LOWER": "into"},  # Match the word 'into'
    {"LOWER": "the"},  # Match the word 'the'
    {"IS_ALPHA": True},  # Match any word (e.g., 'search', 'password', 'email', 'username')
    {"LOWER": {"IN": ["input", "field"]}, "OP": "+"}  # Match 'input', 'field', or both
]
matcher.add("TYPE", [type_pattern])

# Click Command (e.g., 'Click the "Search" button')
click_pattern = [
    {"LOWER": "click"}, {"LOWER": "the"}, {"IS_QUOTE": True, "OP": "?"}, {"IS_ALPHA": True},
    {"IS_QUOTE": True, "OP": "?"},
    {"LOWER": "button"}
]
matcher.add("CLICK", [click_pattern])

# Verify Command (e.g., 'Verify the search results are displayed')
verify_pattern = [
    {"LOWER": "verify"}, {"LOWER": "the"}, {"LOWER": {"IN": ["results", "search"]}}, {"LOWER": "are"},
    {"LOWER": "displayed"}
]
matcher.add("VERIFY", [verify_pattern])


# Function to process the command and extract information
# reflections intelligent functional tester AI
def rift_ai(command: str, page: Page):

    doc = nlp(command)
    matches = matcher(doc)

    for match_id, start, end in matches:
        span = doc[start:end]
        match_label = nlp.vocab.strings[match_id]  # Get command type (OPEN, TYPE, CLICK, VERIFY)

        if match_label == "OPEN":
            # Extract the URL after 'open'
            url = span[-1].text
            print(f"Command: {match_label}, URL: {url}")
            return page.goto(url)

        elif match_label == "TYPE":
            # Extract the typed text (e.g., 'hello', 'secret_sauce', 'admin')
            span = doc[start:end]
            print(f"Matched Command: {span.text}")

            input_text = doc[start + 1:end - 5].text.strip(
                "'")  # Extract the typed text (e.g., 'hello', 'secret_sauce', 'admin')
            field = doc[end - 2].text  # Extract the field descriptor (e.g., 'search', 'password', 'username')
            print(f"Input Text: {input_text}, Field: {field}")

            return find_locator(page, 'input', field).fill(input_text)

        elif match_label == "CLICK":
            # Extract the button text
            button_text = doc[start + 2].text.strip('"')
            print(f"Command: {match_label}, Button Text: {button_text}")

            return find_locator(page, 'input', button_text).click()

        elif match_label == "VERIFY":
            # Just identify the verification step
            print(f"Command: {match_label}")
            return {"command": "verify"}
