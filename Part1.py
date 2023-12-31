"""
PCL 1 Fall Semester 2023 - Course Project
Part 0: Book Selection
Students: Mattia Turra, Mariela Kessler
"""
# --- Imports ---
import os
import re
import json
import spacy
import nltk
# --- You may add other imports here ---



# When creating the JSON strings, we had some issues with our custom class objects, which were resolved by using this CustomEncoder 
class CustomEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that leverages an object's `__json__()` method,
    if available, to obtain its default JSON representation. 
    Source: https://stackoverflow.com/a/24030569
    """

    def default(self, obj):
        """
            Check if class has json attribute and return said obj string if exists
        """
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return json.JSONEncoder.default(self, obj)

# We used three custom classes to improve readibility. We can also these class objects to easily structure the data in the JSOn file
# because we already defined in what relation these classes interact (e.g. a Position object is put into a Occurrence object) 
class Position:
    """
    Custom class for position of occurrence
    start: int
    end: int 
    """

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __json__(self):
        """
        Create json-formatted string (needed because class is custom) 
        """
        return {'start': self.start, 'end': self.end}


class Occurrence:
    """
    Custom class for every occurence of a named entity
    sentence: str
    chapter: str
    boundaries: Position
    """

    def __init__(self, sentence: str, chapter: str, boundaries: Position):
        """
        Initialise Occurrence
        """
        self.sentence = sentence
        self.chapter = chapter,
        self.boundaries = boundaries

    def __json__(self):
        """
        Create json-formatted string (needed because class is custom) 
        """
        return {'sentence': self.sentence, 'chapter': self.chapter, 'Position': self.boundaries}


class NamedBookEntity:
    """
    Custom class for the protagonists and their aliases
    Name: str
    Aliases: str[]
    Occurrences: Occurrence[]
    """

    def __init__(self, name: str, aliases: list[str], occurrences: list[Occurrence]):
        """
        Initialise Named Entity
        """
        self.name = name
        self.aliases = aliases
        self.occurrences = occurrences

    def __json__(self):
        """
        Create json-formatted string (needed because class is custom) 
        """
        return {'name': self.name, 'aliases': self.aliases, 'Occurrences': self.occurrences}

# We didnt manage to implement a dynamic alias identification algorithm (e.g. with tf-idf) so we 
# have to generate a static list of aliases depeing on which book is called
def get_entities_from_book(booktitle:str) -> list[NamedBookEntity]:
    """
        Creates entities for a specific book
        Returns a list of static entities (the main characters)
    """
    entities = list()
    # create list of NamedBookEntity instances with static aliases
    if booktitle == "DrJekyllAndMrHyde":
        entities.extend(
            [NamedBookEntity("Gabriel John Utterson", ["Gabriel", "Gabriel John Utterson", "Utterson", "Mr. Utterson"], list()),
             NamedBookEntity("Richard Enfield", [
                             "Richard Enfield", "Richard", "Enfield", "Mr. Enfield"], list()),
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
        # frankenstein is a peculiar case, becuase the monster has many different names in the books. We did some research and used a collection of those 
        # we had found as aliases for it 
        entities.extend(
            [NamedBookEntity("Victor Frankenstein", ["Victor"], list()),
             NamedBookEntity("The Monster", [
                             "monster", "Monster", "fiend", "wretch", "Wretch", "vile insect", "abhorred monster", "wretched devil", "abhorred devil"], list()),
             NamedBookEntity("Robert Walton", [
                             "seafarer", "Walton", "Robert", "Robert Walton"], list()),
             NamedBookEntity(
                 "Elizabeth Lavenza", ["Elizabeth", "Lavenza", "Elizabeth Lavenza", "orphan"], list()),
             NamedBookEntity("Henry Cleval", [
                             "boyhood friend", "Henry", "Cleval", "Henry Cleval"], list())
             ]
        )
    # return list
    return entities


def clean_text(text: str) -> str:
    """
    Remove escaped new lines and add white spaces to text
    """
    text = text.replace("\n\n", " ")
    return text


def read_text_from_path(path: str) -> str:
    """
    Reads text from filepath and converts it into one string
    """

    with open(path, encoding="utf8") as f:
        lines = f.readlines()
    return "".join(lines)

# Function to process the text and perform NER

# Pretty cookie cutter NER; we generate a new doc from the chapter text and discard all non-PERSON labelled
# entities
def perform_ner(text: str, spacy_model: spacy.language.Language) -> list[spacy.ent]:
    """
    Create spacy.doc from chapter text and extract all PERSON labelled entities
    """
    # create spacy.doc by feeding chapter text into spacy
    doc = spacy_model(text)
    # return all PERSON labelled entites
    return [ent for ent in doc.ents if ent.label_ == "PERSON"]

# Here we used the spacy doc ent from each chapter to add all relevant occurrences to the NamedBookEntity object of the character

# Function to extract and structure entity information
def extract_entity_info(entities_spacy: list[spacy.ent], entities_model: list[NamedBookEntity], chapter: str) -> list[NamedBookEntity]:
    """
    Sieve through all PERSON labelled entities from spacy and
    compare them to the aliases of the custom NamedBookEntity 
    models.
    Return list of custom NamedBookEntity class with all occurrences
    of each character
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

# This wouldnt work for the longest time. We would always get the same results as the standard spacy NER ruler.
# In the end, the reason was formatting error when appending the aliases to the patterns list.
# We are again using all aliases in our NamedBookEntity object and add them as pattern to the entity ruler    

def set_up_spacy(nlp:Language, entity_model:NamedBookEntity) -> Language:
    """
    Add aliases of characters as PERSON labelled entities 
    to Entity Ruler pipeline. Remove existing entity 
    ruler pipeline to not create errors by using aliases
    from other books.
    """
    # Check if 'entity_ruler' component exists in pipeline.
    if nlp.has_pipe("entity_ruler"):
        # If it exists, remove it to avoid conflicts
        nlp.remove_pipe("entity_ruler")

    # Initialise an empty list to store the patterns.
    patterns = []

    # This loop extracts all aliases for each entity.
    aliases_entities = [ent.aliases for ent in entity_model]
    for aliases_entity in aliases_entities:
        for alias in aliases_entity:
            # For each alias, create a pattern dictionary with the label 'PERSON' and the actual alias.
            # These patterns will be used to identify entities in the text.
            patterns.append({"label": "PERSON", "pattern": alias})

    # according to documentation, this config overwrites entities recognized by other components
    config = {
        "overwrite_ents": True,
    }

    # Add new 'entity_ruler' component to pipeline to add custom entities of book.
    ruler = nlp.add_pipe("entity_ruler", config=config)

    # Add patterns to the entity ruler.
    ruler.add_patterns(patterns)

    # Return  pipeline with new entity ruler component.
    return nlp

# Every book is stored in a separate txt file in the same folder
def get_list_of_filenames(folderpath:str) -> list[str]:
    """
    Loads books from provided folder by splitting file names of .txts
    """
    # initialise empty files list
    files = list()
    # get directory from path
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

# As explained above, because we used our own Class objects, we ran into some troubles when creating the JSON file
# so we had to put some effort into seralising our class objects. This wasn't as complicated as we feared it would be
# and we are quite happy with the result.
def save_to_json(data:list[NamedBookEntity], filename:str):
    """
    Saves entity data to json file using CustomEncoder to encode the customs classes
    """
    # transform entity data to json with CustomEncoder
    json_data = json.dumps(data, cls=CustomEncoder)
    # write data to json file
    with open(filename, "w", encoding='utf-8') as jsonfile:
        json.dump(json_data, jsonfile, ensure_ascii=False)
    # return fuck all
    return

# We iterate through all our books and create the NER files all entitites defined in our static list.
# A dynamic solution would have been much cooler, but given time constraints and lack of coverage in 
# the lectures, this could only have been implemented with heavy ChatGPT support, which is not really
# the purpose of this exercise. 
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
        # set up custom entity ruler pipeline
        nlp = set_up_spacy(nlp, entities_model)
        for chapter in chapters:
            # read chapter from file
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
