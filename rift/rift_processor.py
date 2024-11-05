from pathlib import Path

import spacy
from playwright.sync_api import Page, expect

from rift.locator import find_locator
from utils.getProjectRoot import find_project_root

current_file_path = Path(__file__).resolve()
project_root = find_project_root(current_file_path, 'requirements.txt')

print("Project Root:", project_root)
nlp_custom = spacy.load(f"{project_root}/rift/rift_model")


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

    open_commands = ["open", "navigate to", "launch", "go to"]
    type_commands = ["type", "enter", "fill"]
    click_commands = ["clicks", "click"]
    verify_commands = ['verify', 'assert', 'validate']

    if command in open_commands:
        return page.goto(value)
    elif command in type_commands:
        return find_locator(page, 'input', field).fill(value)
    elif command in click_commands:
        if value not in [None, '']:
           return find_locator(page, type_, field, value).locator(f"[value='{value}']").click()
        return find_locator(page, type_, field, value).click()
    elif command in verify_commands:
       if 'page title' in rift_command.lower():
           expect(page).to_have_title(value)
       elif 'url contains' in rift_command.lower():
           expect(page).to_have_url(value)

