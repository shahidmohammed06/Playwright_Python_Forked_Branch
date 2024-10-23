import spacy

# Load the saved model
nlp_custom = spacy.load("rift_model")

# Test the custom NER model on a new sentence
doc = nlp_custom("verify the page title is 'Swag Labs'" )

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
print(f"COMMAND - {command}")
print(f"VALUE - {value}")
print(f"FIELD - {field}")
print(f"TYPE - {type_}")
