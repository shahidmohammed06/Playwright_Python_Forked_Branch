import random

# Define possible replacements
commands = ['click', 'clicks', 'select']
fields = ['login', 'submit', 'register', 'continue', 'proceed', 'enter', 'confirm', 'apply', 'login-lnk', 'lgn-btn',
          'login_lnk', 'lgn_btn']
values = ['male', 'female', 'other', 'abc-123', 'abc_123', 'abc-12#', 'abc_12#']
types = ['button', 'link', 'input', 'label', 'radio button', 'checkbox']

# Generate training data
TRAIN_DATA = []


def get_click_training_data(max_training_data_limit: int):
    for _ in range(max_training_data_limit):
        command = random.choice(commands)
        value = random.choice(values)
        field = random.choice(fields)
        type_ = random.choice(types)

        # Generate variations
        variations = [
            f"{command.lower()} on the {field} {type_}",
            f"{command.lower()} on {field} {type_}",
            f"{command.lower()} on {field} {value} {type_}",
        ]

        # Add unique combinations to training data
        for variation in variations:
            # Calculate the entity indices based on the variation string
            command_start = 0
            command_end = len(command)
            field_start = variation.find(field)
            field_end = field_start + len(field)
            type_start = variation.find(type_)
            type_end = type_start + len(type_)

            # Ensure indices are valid (i.e., not -1 or negative)
            if field_start != -1 and type_start != -1:

                entities = [
                    (command_start, command_end, 'COMMAND'),
                    (field_start, field_end, 'FIELD'),
                    (type_start, type_end, 'TYPE')
                ]

                # Add field only if present
                value_start = variation.find(value)
                if value_start != -1:
                    value_end = value_start + len(value)
                    entities.append((value_start, value_end, 'VALUE'))

                # Append the variation and entities to TRAIN_DATA
                TRAIN_DATA.append((variation, {'entities': entities}))

    return TRAIN_DATA
