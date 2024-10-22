import random

# Define possible replacements
commands = ['click', 'clicks']
values = ['login', 'submit', 'register', 'continue', 'proceed', 'enter', 'confirm', 'apply', 'login-lnk', 'lgn-btn',
          'login_lnk', 'lgn_btn']
types = ['button', 'link', 'input', 'label']

# Generate training data
TRAIN_DATA = []


def get_click_training_data(max_training_data_limit: int):
    for _ in range(max_training_data_limit):
        command = random.choice(commands)
        value = random.choice(values)
        type_ = random.choice(types)

        # Generate variations
        variations = [
            f"{command.lower()} on the {value} {type_}",
            f"{command.lower()} on {value} {type_}",
        ]

        # Add unique combinations to training data
        for variation in variations:
            # Calculate the entity indices based on the variation string
            command_start = 0
            command_end = len(command)
            value_start = variation.find(value)
            value_end = value_start + len(value)
            type_start = variation.find(type_)
            type_end = type_start + len(type_)

            # Ensure indices are valid (i.e., not -1 or negative)
            if value_start != -1 and type_start != -1:
                # Append training data
                TRAIN_DATA.append((variation, {'entities': [
                    (command_start, command_end, 'COMMAND'),
                    (value_start, value_end, 'VALUE'),
                    (type_start, type_end, 'TYPE')
                ]}))

    return TRAIN_DATA
