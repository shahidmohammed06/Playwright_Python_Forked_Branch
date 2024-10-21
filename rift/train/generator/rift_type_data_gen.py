import random

# Define possible replacements
commands = ['Type', 'Enter', 'Fill']
values = ['hello', 'world', 'test', 'data', 'user123', 'input', 'example', 'code', 'key', 'pass']
fields = ['search', 'username', 'firstname', 'email', 'password', 'PIN', 'first-name', 'first_name', 'user-name', 'user_name']
input_types = ['input', 'box', 'input field', 'text box', 'text field', 'input box']

# Generate training data
TRAIN_DATA = []

for _ in range(100):
    command = random.choice(commands)
    value = random.choice(values)
    field = random.choice(fields)
    input_type = random.choice(input_types)

    # Variations for search-related fields
    variations = [
        f"{command} '{value}' into the {field} {input_type}",
        f"{command} '{value}' into {field.replace('input', '')} {input_type}",
    ]

    # Include variations with search input
    if 'search' in field:
        variations.extend([
            f"{command} '{value}' into the search input",
            f"{command} '{value}' into search input"
        ])

    # Add unique combinations to training data
    for variation in variations:
        # Calculate the entity indices based on the variation string
        command_start = 0
        command_end = len(command)
        value_start = variation.find(value)
        value_end = value_start + len(value)
        field_start = variation.find(field)
        field_end = field_start + len(field)

        # Ensure indices are valid (i.e., not -1 or negative)
        if value_start != -1 and field_start != -1:
            # Append training data
            TRAIN_DATA.append((variation, {'entities': [
                (command_start, command_end, 'COMMAND'),
                (value_start, value_end, 'VALUE'),
                (field_start, field_end, 'FIELD')
            ]}))

# Print generated training data
for text, annotations in TRAIN_DATA:
    print(f"(\"{text}\", {annotations}),")
