# your imports go here
#
#
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from types import SimpleNamespace

    
def visualize_character_occurrences_by_chapter(entity_data):
    """
    Visualizes the occurrences of characters in chapters.

    Args:
    entity_data: A list of entities (characters) with their occurrences in chapters.
    """

    occurrences_of_characters = {}
    
    # We start with the data from the JSON file, where all detected entity occurrences are stored including the sentences they appear in.
    
    # Loop through each character in the entity data
    for main_character in entity_data:
        # Extract the name of the character
        char_name = main_character.name

        
        # Initialize a dictionary to count occurrences per chapter for this character (the typo is left in on purpose)
        occurence_per_chapter = dict()

        # Loop through each occurrence of the entity
        for occurrence in main_character.Occurrences:
            # Extract the chapter key (e.g., 'Chapter_1') from the occurrence data
            chapter_key = occurrence.chapter[0]

            # Increment the count for this chapter, or initialize it to 1 if not already present
            if chapter_key in occurence_per_chapter:
                occurence_per_chapter[chapter_key] += 1
            else:
                occurence_per_chapter[chapter_key] = 1

        # We struggled to find a satisfying solution for sorting the chapters in our data, so we used ChatGPT which generated a 
        # slick lambda expressions that extracts the integer from the chapter name and uses that for sorting the occurrences
        
        # Sort the chapters numerically and convert back to a dictionary
        sorted_chapters = sorted(occurence_per_chapter.items(), key=lambda x: int(x[0].split('_')[-1]))
        occurence_per_chapter = dict(sorted_chapters)

        # this sorted list is then saved adn replaces the unsorted list
        # Add the sorted chapter occurrences to the main dictionary under the character's name
        occurrences_of_characters[char_name] = occurence_per_chapter

    # Create a set to collect all unique chapter names across all characters
    all_chapters = set()
    for character in occurrences_of_characters.values():
        all_chapters.update(character.keys())

    
    # We use an adapted version of the lambda expression from above to sort the set of all chapters
    # Sort the chapter names numerically to determine the column order for the DataFrame
    sorted_chapters = sorted(all_chapters, key=lambda x: int(x.split('_')[-1]))

    # The dict we have created is fed into a DataFrame object, which we will use to visualise the occurrences
    # per entity.
    # Create a DataFrame from the occurrences data with characters as rows and chapters as columns
    heatmap_data = pd.DataFrame.from_dict(occurrences_of_characters, orient="index", columns=sorted_chapters)

    # Create and configure a heatmap visualization
    
    # We fiddled around with the size of the window a bit, but decided that 15x10 works well for all three books
    plt.figure(figsize=(15, 10))
    # Seaborn has a built in heatmap functionality, which is a great way to visualise the quantity of entity occurrences
    # viridis is a popular colormap used in heat maps which we saw in some code examples, so we used it too  
    sns.heatmap(heatmap_data, annot=True, cmap='viridis')
    # Here we defined the plot title and the dimension labels
    plt.title('Character Occurrences by Chapter')
    plt.ylabel('Character')
    plt.xlabel('Chapter')
    # this shows the labels of the x axis diagonally, so they dont cover each other
    plt.xticks(rotation=45)
    plt.show()



# main function
def main():
    #book = "DrJekyllAndMrHyde"
    #book = "dracula"
    book = "frankenstein"
    entity_data = ""
    # Load your JSON data
    with open(f'{book}_MainCharacters_NER.json', 'r') as file:
        data = json.load(file)
        entity_data = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

    # plot chapter occurrences per entity:
    visualize_character_occurrences_by_chapter(entity_data)


# Run the main function
if __name__ == "__main__":
    main()