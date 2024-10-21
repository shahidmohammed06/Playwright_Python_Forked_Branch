import spacy

# Load the saved model
nlp_custom = spacy.load("rift_model")

# Test the custom NER model on a new sentence
doc = nlp_custom("Click on the Login button")

# Initialize variables to hold the extracted entities
command = None
value = None
field = None
type_ = None

# Iterate through detected entities and assign to variables
for ent in doc.ents:
    if ent.label_ == "COMMAND":
        command = ent.text
    elif ent.label_ == "VALUE":
        value = ent.text
    elif ent.label_ == "FIELD":
        field = ent.text
    elif ent.label_ == "TYPE":
        type_ = ent.text

# Print the extracted entities
print(f"Command {command}")
print(f"{value} VALUE")
print(f"{field} FIELD")
print(f"{type_} TYPE")
