import spacy
from playwright.sync_api import Page

from rift.locator import find_locator

nlp_custom = spacy.load("D:\projects\playwright-python\\rift\\rift_model")


# Function to process the command and extract information
# reflections intelligent functional tester AI
def rift_ai(rift_command: str, page: Page):

    doc = nlp_custom(rift_command)

    command = None
    value = None
    field = None
    type_ = None

    for ent in doc.ents:
        if ent.label_ == "COMMAND":
            command = ent.text.lower()
        elif ent.label_ == "VALUE":
            value = ent.text
        elif ent.label_ == "FIELD":
            field = ent.text
        elif ent.label_ == "TYPE":
            type_ = ent.text

    open_commands = ["open", "navigate", "launch", "go to"]
    type_commands = ["type", "enter", "fill"]
    click_commands = ["clicks", "click"]

    if command in open_commands:
        return page.goto(value)
    elif command in type_commands:
        return find_locator(page, 'input', field).fill(value)
    elif command in click_commands:
        return find_locator(page, 'input', value).click()

