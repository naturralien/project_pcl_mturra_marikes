# TODO: Visualization 2
# Load your JSON data
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from types import SimpleNamespace

with open('frankenstein_MainCharacters_NER.json', 'r') as file:
    data = json.load(file)
entity_data =  json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

# Initialize a dictionary to store character occurrences
occurrences_of_characters = {}

# Loop through each character in the JSON data
for main_character in entity_data:
    char_name = main_character.name
    occurence_per_chapter = dict()
    for occurrence in main_character.Occurrences:
        chapter_key = occurrence.chapter[0]
        if chapter_key in occurence_per_chapter:
            occurence_per_chapter[chapter_key] += 1
        else:
            occurence_per_chapter[chapter_key] = 1

    # Sort chapters numerically while maintaining occurrence counts
    sorted_chapters = sorted(occurence_per_chapter.items(), key=lambda x: int(x[0].split('_')[-1]))
    occurence_per_chapter = dict(sorted_chapters)

    occurrences_of_characters[char_name] = occurence_per_chapter

all_chapters = set()
for character in occurrences_of_characters.values():
    all_chapters.update(character.keys())

sorted_chapters = sorted(all_chapters, key=lambda x: int(x.split('_')[-1]))

# Create a DataFrame from the occurrences data
heatmap_data = pd.DataFrame.from_dict(occurrences_of_characters, orient="index", columns=sorted_chapters)

# Create heatmap
plt.figure(figsize=(15, 10))  # Adjust size as needed
sns.heatmap(heatmap_data, annot=True, cmap='viridis')
plt.title('Character Occurrences by Chapter')
plt.ylabel('Character')
plt.xlabel('Chapter')
plt.xticks(rotation=45)  # Rotate chapter labels for better readability
plt.show()