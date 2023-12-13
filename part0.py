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
    data =
    #list to store words
    result_data = []
    #to get the individual words as dictionary in sentiment file
    if data.includes('Sentiment'):
        for content in data:
            words = content.strip().split(',')
            result_data.extend([{'Adj': word} for word in words])
            # remove the last element of the list because it's empty
            result_data.pop()

    #to get the individual words as dictionary in entities file
    elif data.includes('Entities'):
        for content in data:
            words = content.strip().split(',')
            result_data.extend([{'Name': word} for word in words])
            # remove the last element of the list because it's empty
            result_data.pop()

    return json.dumps(result_data) #return the json string
    #pass


def write_as_json(data, file_path):
    """
    Create a function to write your json string to a file here.
    Think about a naming convention for the output files.
    """
    # if path ends with Sentiment (Sentiment folder with txt files)
    if file_path.endswith('Sentiment'):
        # iterate over the files in the folder
        for data in os.path.dirname(file_path):
            # open the file and save as json file
            with open(file_path, 'w') as sentiment_outfile:
                json.dump(data, sentiment_outfile)


    # if path ends with Entities (Entities folder with txt files)
    elif file_path.endswith('Entities'):
        # iterate over the files in the folder
        for data in os.path.dirname(file_path):
            # open the file and save as json file
            with open(file_path, 'w') as entities_outfile:
                json.dump(data, entities_outfile)
    #pass

def create_entities_sentiment_folders(path):
    """
    Create folders to store json files for Entities and Sentiment Analysis
    """
    # create entities_json or sentiment_json folder

    sentiment_folder = os.path.join(path, 'sentiment_json')
    if not os.path.exists(sentiment_folder):
        os.makedirs(sentiment_folder)
    return sentiment_folder
    entities_folder = os.path.join(path, 'entities_json')
    if not os.path.exists(entities_folder):
        os.makedirs(entities_folder)
    return entities_folder

def main():
    # Here you may add the neccessary code to call your functions, and all the steps before, in between, and after calling them.
    """
    output_folder = 'output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    pass
    """

# This is the standard boilerplate that calls the main() function when the program is executed.
if __name__ == '__main__':
    main()
