import os
import random

import spacy
from spacy.training import Example

from rift.train.generator.rift_click_data_gen import get_click_training_data
from rift.train.generator.rift_open_data_gen import get_open_training_data
from rift.train.generator.rift_type_data_gen import get_type_training_data
from rift.train.generator.rift_verify_data_gen import get_verify_training_data

# Increase the amount of training data
TRAIN_DATA = []

max_training_data_limit = 100

TRAIN_DATA.extend(get_type_training_data(max_training_data_limit))
TRAIN_DATA.extend(get_click_training_data(max_training_data_limit))
TRAIN_DATA.extend(get_open_training_data(max_training_data_limit))
TRAIN_DATA.extend(get_verify_training_data(max_training_data_limit))


# Load a blank English model
current_script_path = os.path.dirname(os.path.abspath(__file__))  # Get the current script directory
project_root = os.path.join(current_script_path, '..', 'rift_model')  # Navigate to the parent and access 'rift'

nlp = spacy.blank('en')

# Add the Named Entity Recognizer to the pipeline
ner = nlp.add_pipe("ner")

# Add the custom entity labels to the NER
ner.add_label("COMMAND")
ner.add_label("VALUE")
ner.add_label("FIELD")
ner.add_label("TYPE")

# Prepare the training
optimizer = nlp.begin_training()

# Train the NER model for a few iterations
for i in range(50):
    random.shuffle(TRAIN_DATA)
    losses = {}
    for text, annotations in TRAIN_DATA:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update([example], losses=losses, drop=0.5)  # Update the model with the training data
    print(f"Iteration {i + 1}, Losses: {losses}")

# Save the trained model to disk
nlp.to_disk(project_root)
