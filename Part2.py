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
from nrclex import NRCLex
import argparse
from types import SimpleNamespace

# Feel free to add more functions as needed!


# Function to perform sentiment analysis
def analyze_sentiment(text, analyzer=None):
    # TODO: Apply the sentiment analysis tool to the text and return the results

    # takes text as input and returns a dictionary of emotions and their frequencies
    book_text = NRCLex(text)
    # if analyzer is not default, then return the respective results
    if analyzer is not None:
        if analyzer == 'emotion':
            sentiment_results = book_text.raw_emotion_scores
        elif analyzer == 'emotion_intensity':
            sentiment_results = book_text.affect_intensity
        elif analyzer == 'top_emotions':
            sentiment_results = book_text.top_emotions
    # using the default analyzer for sentiment analysis
    else:
        sentiment_results = book_text.affect_frequencies

    # returns the sentiment results and the analyzer used
    return sentiment_results, analyzer


# Function to save sentiment analysis results to a JSON file
def save_sentiment_results(results, filename):
    # TODO: Save the sentiment analysis results in a structured JSON format:
    def convert_keys(obj):
        if isinstance(obj, tuple):
            return str(obj)
        elif isinstance(obj, dict):
            return {str(key): convert_keys(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_keys(element) for element in obj]
        else:
            return obj

    #saves sentiment analysis in json file
    with open(filename, 'w', encoding='utf-8') as output_file:
        json.dump(results, output_file, indent=2, default=str)


# Main function
def main():

    # TODO: Load or define the text for analysis
    #text = "Your text for sentiment analysis."
    parser = argparse.ArgumentParser(description='Perform sentiment analysis on given txt file.')
    parser.add_argument('file_path', help='Path to json file to be analyzed.')
    args = parser.parse_args()
    try:
        with open(args.file_path, 'r', encoding='utf-8') as file:
            text = json.load(file)
            entity_data = json.loads(text, object_hook=lambda d: SimpleNamespace(**d))
    except FileNotFoundError:
        print('File not found. Please check your path and try again.')
        exit()
        return

    # TODO: Perform sentiment analysis on the text using your chosen tool
    # For example, analyze each sentence or paragraph where entities are identified
    all_results = dict()
    aggregated_scores_of_entire_book = dict()

    for main_character in entity_data:
        char_name = main_character.name
        #occurrence_per_chapter = dict()

        #dictionary to store aggregated sentiment per chapter
        sentiment_scores_per_chapter = dict()

        #print(f'Analyzing sentiment for {char_name}')

        for occurrence in main_character.Occurrences:

            # converting it to string
            chapter_key = str(occurrence.chapter)

            # Analyze the sentiment of the sentence
            sentence_sentiments, _ = analyze_sentiment(occurrence.sentence)
            # Add the sentiment scores to the dictionary
            if chapter_key not in sentiment_scores_per_chapter:
                sentiment_scores_per_chapter[chapter_key] = dict()

            for emotion, score in sentence_sentiments.items():
                sentiment_scores_per_chapter[chapter_key][emotion] = \
                    sentiment_scores_per_chapter[chapter_key].get(emotion, 0) + score


        #dictionary filled with sum of all scores for each emotion per chapter for the whole book
        aggregated_scores = dict()
        for chapter, chapter_scores in sentiment_scores_per_chapter.items():
            for emotion, score in chapter_scores.items():
                aggregated_scores[emotion] = aggregated_scores.get(emotion, 0) + score
        results = {
            char_name: {
                'sentiment_per_chapter': sentiment_scores_per_chapter,
                'aggregated_scores_in_chapters': aggregated_scores
            }
        }

        # Add the results for all characters to the dictionary
        all_results.update(results)

    #Calculate the sentiment scores of the entire book
    for char_name, char_data in all_results.items():
        for chapter, chapter_scores in char_data['sentiment_per_chapter'].items():
            for emotion, score in chapter_scores.items():
                aggregated_scores_of_entire_book[emotion] = \
                    aggregated_scores_of_entire_book.get(emotion, 0) + score

        # Add the aggregated scores for the full book to the dictionary
    all_results['Aggregated_sentiments_for_the_full_book'] = {
        'aggregated_scores': aggregated_scores_of_entire_book
    }

    # Save the results to a JSON file
    # naming newly generated json file
    book_name = os.path.basename(args.file_path).split('.')[0].replace('_MainCharacters_NER', '')

    # Example filename: 'BookTitle_Sentiment.json'
    json_filename = f'{book_name}_Sentiment.json'

    # saving results to json file
    save_sentiment_results(all_results, json_filename)


# Run the main function
if __name__ == "__main__":
    main()