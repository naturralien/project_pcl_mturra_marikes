"""
PCL 1 Fall Semester 2023 - Course Project
Part 0: Book Selection
Students: <person 1>, <person 2>
"""
# --- Imports ---
import os
import re
import json
import spacy
import nltk
# --- You may add other imports here ---
import jsonpickle



# TODO: Load the spaCy model
# TODO: Load the book text

class MyEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that leverages an object's `__json__()` method,
    if available, to obtain its default JSON representation. 

    """
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return json.JSONEncoder.default(self, obj)

class Position:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
    def __json__(self):
        return {'start': self.start, 'chapter': self.end}


class Occurrence:
    def __init__(self, sentence, chapter, boundaries):
        self.sentence = sentence
        self.chapter = chapter,
        self.boundaries = boundaries

    def __json__(self):
        return {'sentence': self.sentence, 'chapter': self.chapter, 'Position': self.boundaries}

class NamedBookEntity:
    def __init__(self, name, aliases, occurrences):
        self.name = name
        self.aliases = aliases
        self.occurrences = occurrences

    def __json__(self):
        return {'name': self.name, 'aliases': self.aliases, 'Occurrences': self.occurrences}

def create_entities(booktitle):
    entities = []
    if booktitle:
        entities.extend(
            [NamedBookEntity("Gabriel John Utterson",["Utterson", "Mr. Utterson"], list()),
            NamedBookEntity("Richard Enfield",["Richard Enfield", "Richard" , "Enfield"], list()),
            NamedBookEntity("Dr. Henry Jekyll",["Jekyll", "Henry Jekyll", "Mr. Jekyll", "Dr. Jekyll"], list()),
            NamedBookEntity("Edward Hyde",["Hyde", "Edward Hyde", "Edward", "Mr. Hyde"], list()),
            NamedBookEntity("Dr. Hastie Lanyon", ["Dr. Lanyon", "Lanyon", "Hastie", "Mr. Lanyon"], list())
            ]
        )
    return entities

def get_entities_from_book(booktitle):
    entities = create_entities(booktitle) 
    return entities


def clean_text(text):
    text = text.replace("\n\n"," ")
    return text


def read_text_from_path(path):
    """
    Reads text from filepath and converts it into one string
    """

    with open(path, encoding="utf8") as f:
        lines = f.readlines()
    return "".join(lines)

# Feel free to add more functions as needed!


# Function to process the text and perform NER
def perform_ner(text, spacy_model):
    # TODO: Process the text using the provided model and return the entities
    # Example: return nlp_model(text).ents
    entities = []
    doc = spacy_model(text)
    return [ent for ent in doc.ents if ent.label_ == "PERSON"] 


# Function to extract and structure entity information
def extract_entity_info(entities):
    entity_data = create_entities("TODO")

    for entity in entities:
        for character in entity_data:
            if entity.text in character.aliases:
                character.occurrences.append(
                    Occurrence(str(entity.sent), "TODO", Position(int(entity.start_char),int(entity.end_char)))
                )
    # TODO: Iterate over entities and extract necessary information
    # Append the extracted info to entity_data
    return entity_data


# Function to save data to JSON file
def save_to_json(data, filename):
    # TODO: Save the data to a JSON file
    json_data = json.dumps(data, cls=MyEncoder)
    with open(filename,"w", encoding='utf-8') as jsonfile:
        json.dump(json_data,jsonfile,ensure_ascii=False)
    return


# Main Function
def main():
    # TODO: Load your book text here
    book_text = clean_text(read_text_from_path("DrJekyllAndMrHyde\chapters\Chapter_1.txt"))
    nlp = spacy.load('en_core_web_sm') 

    # Perform NER on the text
    entities = perform_ner(book_text, nlp)

    # Extract information from entities
    entity_info = extract_entity_info(entities)

    # Save the results to a JSON file
    save_to_json(entity_info, 'DrJekyllAndMrHyde_Chapter1_NER.json')


# Run the main function
if __name__ == "__main__":
    main()
