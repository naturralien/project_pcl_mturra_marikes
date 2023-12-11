"""
PCL 1 Fall Semester 2023 - Course Project
Part 0: Book Selection
Students: Mattia Turra, Mariela Kessler
"""

# --- Imports ---
import os
import re
import json
# --- Don't add other imports here ---


def json_conversion(data):
    """
    Create a function to convert the data to a json string here"""
    return json.dumps(data)
    #pass


def write_as_json(data, file_path):
    """
    Create a function to write your json string to a file here.
    Think about a naming convention for the output files.
    """
    if file_path.includes('sentiment'):
        with open(file_path, 'w') as sentiment_outfile:
            json.dump(data, sentiment_outfile)

    elif file_path.includes('entities'):
        with open(file_path, 'w') as entities_outfile:
            json.dump(data, entities_outfile)
    #pass


def main():
    # Here you may add the neccessary code to call your functions, and all the steps before, in between, and after calling them.
    output_folder = 'output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    pass


# This is the standard boilerplate that calls the main() function when the program is executed.
if __name__ == '__main__':
    main()
