import random

# Define possible replacements
commands = ['verify', 'assert', 'validate']
values = ['hello', 'world', 'test', 'data', 'user123', 'Swag Labs', 'Google Search Page']
fields = ['search', 'username', 'firstname']
element_types = ['input', 'button', 'div', 'h1']


TRAIN_DATA = []

def get_verify_training_data(max_training_data_limit: int):

    for _ in range(max_training_data_limit):

        command = random.choice(commands)
        value = random.choice(values)
        field = random.choice(fields)
        element_type = random.choice(element_types)

        # Variations for search-related fields
        variations = [
            f"{command} the page title is '{value}'",
            f"{command} the URL contains '{value}'",
            f"{command} the {field} {element_type} text is '{value}'",
            f"{command} the {field} {element_type} has text '{value}'",
            f"{command} the {field} {element_type} is visible",
        ]

        # Add unique combinations to training data
        for variation in variations:
            # Calculate the entity indices based on the variation string
            command_start = 0
            command_end = len(command)
            value_start = variation.find(value)
            value_end = value_start + len(value)

            if value_start != -1:

                entities = [
                    (command_start, command_end, 'COMMAND'),
                    (value_start, value_end, 'VALUE')
                ]

                # Add field only if present
                field_start = variation.find(field)
                if field_start != -1:
                    field_end = field_start + len(field)
                    entities.append((field_start, field_end, 'FIELD'))

                # Add element_type only if present
                element_type_start = variation.find(element_type)
                if element_type_start != -1:
                    element_type_end = element_type_start + len(element_type)
                    entities.append((element_type_start, element_type_end, 'TYPE'))

                # Append the variation and entities to TRAIN_DATA
                TRAIN_DATA.append((variation, {'entities': entities}))

    return TRAIN_DATA
