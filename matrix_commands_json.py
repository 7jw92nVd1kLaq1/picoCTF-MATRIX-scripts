import json

def create_dict_and_output_json(file_path, output_json_path):
    data_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            columns = line.split()
            if len(columns) >= 2:  # Ensure there are at least two columns
                key = columns[0]
                value = columns[1]
                data_dict[key] = value

    # Write the dictionary to a JSON file
    with open(output_json_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)

# Specify the path to your file and the output JSON file path
file_path = './matrix_commands'
output_json_path = './matrix_commands.json'

# Call the function
create_dict_and_output_json(file_path, output_json_path)

