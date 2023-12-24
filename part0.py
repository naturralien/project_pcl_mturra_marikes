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

    # list to store words
    result_data = []
    
    # to get the individual words as dictionary in sentiment file
    print("Data before processing: ", data)
    
    for content in data:
        words = content.strip().split(',')
        result_data.extend([{'PROPN': word} for word in words])
        result_data.pop()  # remove the last element of the list because it's empty
    print("Data after processing: ", result_data)
    return json.dumps(result_data)


def write_as_json(data, file_path):
    """
    Create a function to write your json string to a file here.
    Think about a naming convention for the output files.
    """
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)


def create_entities_sentiment_folders(book_path):
    """
    #Create folders to store json files for Entities and Sentiment Analysis
    """
    entities_folder = None
    sentiment_folder = None

    # create entities_json or sentiment_json folder
    if book_path.endswith('sentiments'):
        sentiment_folder = os.path.join(book_path.replace('sentiments', 'sentiment_json'))
        if not os.path.exists(sentiment_folder):
            os.makedirs(sentiment_folder)

        # sentiment_folder = None # to avoid UnboundLocalError

    elif book_path.endswith('entities'):
        entities_folder = os.path.join(book_path.replace('entities', 'entities_json'))
        if not os.path.exists(entities_folder):
            os.makedirs(entities_folder)
        # entities_folder = None # to avoid UnboundLocalError

    return entities_folder, sentiment_folder

def main():
    # Here you may add the neccessary code to call your functions, and all the steps before, in between, and after calling them.

    book_path = input("Enter the book path: ").strip()

    entities_folder, sentiment_folder = create_entities_sentiment_folders(book_path)

    for file_name in os.listdir(book_path):
        file_path = os.path.join(book_path, file_name)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as infile:
                data = infile.readlines()

            data_type = 'entities' if 'entities' in book_path else 'sentiments'
            # json_data = json_conversion(data)
            output_folder = entities_folder if data_type == 'entities' else sentiment_folder
            output_path = os.path.join(output_folder, f"{file_name.replace('.txt', '.json')}")
            output_path = os.path.join(output_folder, f"{file_name.replace('.txt', '.json')}")

            json_data = json_conversion(data)
            write_as_json(json_data, output_path)

# This is the standard boilerplate that calls the main() function when the program is executed.
if __name__ == '__main__':
    main()
