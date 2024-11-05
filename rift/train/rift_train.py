import os
import random
import concurrent.futures
import time  # Import time to track execution time

import spacy
from spacy.training import Example

from rift.train.generator.rift_click_data_gen import get_click_training_data
from rift.train.generator.rift_open_data_gen import get_open_training_data
from rift.train.generator.rift_type_data_gen import get_type_training_data
from rift.train.generator.rift_verify_data_gen import get_verify_training_data

# Increase the amount of training data
TRAIN_DATA = []

max_training_data_limit = 50

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


def train_on_example(text, annotations):
    losses = {}
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, annotations)
    nlp.update([example], losses=losses, drop=0.5)  # Update the model with the training data
    return losses


# Capture the start time for the entire training process
overall_start_time = time.time()

# Train the NER model for a few iterations
for i in range(15):
    iteration_start_time = time.time()  # Start time for each iteration

    random.shuffle(TRAIN_DATA)
    overall_losses = {"ner": 0.0}  # Accumulator for overall losses

    # Use ThreadPoolExecutor to train on the entire dataset in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(train_on_example, text, annotations) for text, annotations in TRAIN_DATA]

        for future in concurrent.futures.as_completed(futures):
            losses = future.result()  # Retrieve the losses from each thread

            # Accumulate the loss for the NER component
            overall_losses["ner"] += losses.get("ner", 0.0)

    # Calculate the time taken for this iteration
    iteration_end_time = time.time()
    iteration_duration = iteration_end_time - iteration_start_time

    print(f"Iteration {i + 1} completed. Overall Loss: {overall_losses['ner']:.4f}. "
          f"Iteration Time: {iteration_duration:.2f} seconds.")

# Capture the end time for the entire training process
overall_end_time = time.time()

# Calculate total time taken for training
total_duration = overall_end_time - overall_start_time
print(f"Training completed. Total time taken: {total_duration:.2f} seconds.")

# Save the trained model to disk
nlp.to_disk(project_root)
