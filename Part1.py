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


# TODO: Load the spaCy model
# TODO: Load the book text

class CustomEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that leverages an object's `__json__()` method,
    if available, to obtain its default JSON representation. 
    Source: https://stackoverflow.com/a/24030569
    """

    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return json.JSONEncoder.default(self, obj)


class Position:
    """
    Custom class for position of occurrence
    start: int
    end: int 
    """

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __json__(self):
        return {'start': self.start, 'end': self.end}


class Occurrence:
    """
    Custom class for every occurence of a named entity
    sentence: str
    chapter: str
    boundaries: Position
    """

    def __init__(self, sentence, chapter, boundaries):
        self.sentence = sentence
        self.chapter = chapter,
        self.boundaries = boundaries

    def __json__(self):
        return {'sentence': self.sentence, 'chapter': self.chapter, 'Position': self.boundaries}


class NamedBookEntity:
    """
    Custom class for the protagonists and their aliases
    Name: str
    Aliases: str[]
    Occurrences: Occurrence[]
    """

    def __init__(self, name, aliases, occurrences):
        self.name = name
        self.aliases = aliases
        self.occurrences = occurrences

    def __json__(self):
        return {'name': self.name, 'aliases': self.aliases, 'Occurrences': self.occurrences}


def get_entities_from_book(booktitle):
    """
        Creates entities for a specific book
        Returns a list of static entities (the main characters)
    """
    entities = list()
    if booktitle == "DrJekyllAndMrHyde":
        entities.extend(
            [NamedBookEntity("Gabriel John Utterson", ["Utterson", "Mr. Utterson"], list()),
             NamedBookEntity("Richard Enfield", [
                             "Richard Enfield", "Richard", "Enfield"], list()),
             NamedBookEntity("Dr. Henry Jekyll", [
                             "Jekyll", "Henry Jekyll", "Mr. Jekyll", "Dr. Jekyll"], list()),
             NamedBookEntity(
                 "Edward Hyde", ["Hyde", "Edward Hyde", "Edward", "Mr. Hyde"], list()),
             NamedBookEntity("Dr. Hastie Lanyon", [
                             "Dr. Lanyon", "Lanyon", "Hastie", "Mr. Lanyon"], list())
             ])
    elif (booktitle == "dracula"):
         entities.extend(
            [NamedBookEntity("Count Dracula", ["Dracula", "Count Dracula"], list()),
             NamedBookEntity("Van Helsing", [
                             "Van Helsing", "Helsing"], list()),
             NamedBookEntity("Jonathan Harker", [
                             "Jonathan Harker", "Jonathan", "Harker"], list()),
             NamedBookEntity("Mina Murray", [
                "Mina", "Murray", "Mina Harker", "MINA"], list()),
             NamedBookEntity("Lucy Westenra", [
                             "Lucy", "Westenra", "Lucy Westenra"], list()),
            NamedBookEntity("Dr. John Seward", [
                             "Dr. John Seward", "John", "Seward", "Dr. Seward"], list()),
            NamedBookEntity("Arthur Holmwood", [
                             "Arthur Holmwood", "Arthur", "Holmwood", "Mr. Holmwood"], list())                         
             ]     
        )
    elif (booktitle == "frankenstein"):
        entities.extend(
            [NamedBookEntity("Victor Frankenstein", ["Victor"], list()),
             NamedBookEntity("The Monster", [
                             "monster", "Monster", "fiend", "wretch", "Wretch", "vile insect", "abhorred monster", "wrteched devil", "abhorred devil"], list()),
             NamedBookEntity("Robert Walton", [
                             "seafarer", "Walton", "Robert", "Robert Walton"], list()),
             NamedBookEntity(
                 "Elizabeth Lavenza", ["Elizabeth", "Lavenza", "Elizabeth Lavenza", "orphan"], list()),
             NamedBookEntity("Henry Cleval", [
                             "boyhood friend", "Henry", "Cleval", "Henry Cleval"], list())
             ]    
        )
    return entities


def clean_text(text):
    text = text.replace("\n\n", " ")
    return text


def read_text_from_path(path):
    """
    Reads text from filepath and converts it into one string
    """

    with open(path, encoding="utf8") as f:
        lines = f.readlines()
    return "".join(lines)

# Function to process the text and perform NER


def perform_ner(text, spacy_model):
    """
    Create spacy.doc from text and extract all PERSON labelled entities
    """
    doc = spacy_model(text)
    return [ent for ent in doc.ents if ent.label_ == "PERSON"]


# Function to extract and structure entity information
def extract_entity_info(entities_spacy, entities_model, chapter):
    """

    """
    # loop through spacy.ent list
    for entity in entities_spacy:
        # loop through NamedBookEntity (custom class) list
        for character in entities_model:
            # condition if ent object texts appears in aliases list
            if entity.text in character.aliases:
                # add occurrence attributes to Occurrence list of NamedBookEntity
                character.occurrences.append(
                    Occurrence(str(entity.sent), chapter, Position(
                        int(entity.start_char), int(entity.end_char)))
                )
    return entities_model


def get_list_of_filenames(folderpath):
    """
    Loads books from provided folder by splitting file names of .txts
    """
    # initialise empty files list
    files = list()
    # get directory from argument
    directory = os.fsencode(folderpath)
    # loop through directory
    for file in os.listdir(directory):
        # get filename from file
        filename = os.fsdecode(file)
        # split filename from extension and add substring to files list
        files.append(filename.split(".")[0])
    # return list of file names
    return files

# Function to save data to JSON file


def save_to_json(data, filename):
    """
    Saves entity data to json file using CustomEncoder to encode the customs classes
    """
    # transform entity data to json with CustomEncoder
    json_data = json.dumps(data, cls=CustomEncoder)
    # write data to json file
    with open(filename, "w", encoding='utf-8') as jsonfile:
        json.dump(json_data, jsonfile, ensure_ascii=False)
    # return fuckall
    return


# Main Function
def main():
    # Load list of books from folder
    books = get_list_of_filenames("Books")

    # initialise english spacy model
    nlp = spacy.load('en_core_web_sm')

    # iterate through the books
    for book in books:
        # get list of chapter from directory
        chapters = get_list_of_filenames(f"{book}\chapters")
        # load new NamedBookEntity from booktitkle
        entities_model = get_entities_from_book(book)
        for chapter in chapters:
            chapter_text = clean_text(read_text_from_path(
                f"{book}\chapters\{chapter}.txt"))
            # Perform NER on the text
            entities_spacy = perform_ner(chapter_text, nlp)

            # Extract information from entities
            entitiesModel = extract_entity_info(
                entities_spacy, entities_model, chapter)

        # Save the results to a JSON file
        save_to_json(entitiesModel, f'{book}_MainCharacters_NER.json')


# Run the main function
if __name__ == "__main__":
    main()
