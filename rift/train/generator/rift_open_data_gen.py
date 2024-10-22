import random

# Define possible replacements
commands = ['open', 'launch', 'go to', 'navigate to']
values = ['https://www.google.com', 'https://yahoo.com', 'https://gmail.com']

# Generate training data
TRAIN_DATA = []

def get_open_training_data(max_training_data_limit: int):

    for _ in range(max_training_data_limit):
        command = random.choice(commands)
        value = random.choice(values)

        # Generate variations
        variations = [
            f"{command.lower()} {value}",
        ]

        # Add unique combinations to training data
        for variation in variations:
            # Calculate the entity indices based on the variation string
            command_start = 0
            command_end = len(command)
            value_start = variation.find(value)
            value_end = value_start + len(value)

            # Ensure indices are valid (i.e., not -1 or negative)
            if value_start != -1:
                # Append training data
                TRAIN_DATA.append((variation, {'entities': [
                    (command_start, command_end, 'COMMAND'),
                    (value_start, value_end, 'VALUE'),
                ]}))

    return TRAIN_DATA

