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
        if occurence_per_chapter.get(occurrence.chapter[0]):
            occurence_per_chapter[occurrence.chapter[0]] += 1
        else:
            occurence_per_chapter.update({f"{occurrence.chapter[0]}": 1})
    occurrences_of_characters[char_name] = occurence_per_chapter
    print(occurrences_of_characters)

# Create a DataFrame from the occurrences data
heatmap_data = pd.DataFrame.from_dict(occurrences_of_characters, orient="index")

# Create heatmap
plt.figure(figsize=(15, 10))  # Adjust size as needed
sns.heatmap(heatmap_data, annot=True, cmap='viridis')
plt.title('Character Occurrences by Chapter')
plt.ylabel('Character')
plt.xlabel('Chapter')
plt.xticks(rotation=45)  # Rotate chapter labels for better readability
plt.show()