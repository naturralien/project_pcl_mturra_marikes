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

    with open(filename, 'w', encoding='utf-8') as output_file:
        json.dump(results, output_file, indent=2)
    #pass


# Main function
def main():

    # TODO: Load or define the text for analysis
    #text = "I hate you" #"Your text for sentiment analysis."
    parser = argparse.ArgumentParser(description='Perform sentiment analysis on given txt file.')
    parser.add_argument('file_path', help='Path to txt file to be analyzed.')
    args = parser.parse_args()
    try:
        with open(args.file_path, 'r', encoding='utf-8') as file:
            text = json.load(file)
            entity_data = json.loads(text, object_hook=lambda d: SimpleNamespace(**d))
    except FileNotFoundError:
        print('File not found. Please check your path and try again.')
        exit()
        return

    for main_character in entity_data:
        char_name = main_character.name
        occurrence_per_chapter = dict()
        sentiment_scores_per_sentence = dict()

        #print(f'Analyzing sentiment for {char_name}')

        for occurrence in main_character.Occurrences:

            # converting it to tuple because list is not hashable
            chapter_key = tuple(occurrence.chapter)

            # Analyze the sentiment of the sentence
            sentence_sentiments, _ = analyze_sentiment(occurrence.sentence)
            sentence_key = f'For {chapter_key}, Sentence: \'{occurrence.sentence}\'' #added
            sentiment_scores_per_sentence[sentence_key] = sentence_sentiments

            for sentence_num, (key, sentiment_scores) in enumerate(sentiment_scores_per_sentence.items(), start=1):
                # for easier reading
                print()
        print(f'The sentiment scores associated with {char_name} are:')
        for sentence_key, sentiment_scores in sentiment_scores_per_sentence.items():  # changed list to scores

            print(f'{sentence_key}, the sentiments are: {sentiment_scores}')
            print()

        aggregated_scores = dict()
        for sentence_key, sentiment_scores in sentiment_scores_per_sentence.items():
            for emotion, score in sentiment_scores.items():
                aggregated_scores[emotion] = aggregated_scores.get(emotion, 0) + score
        results = {
            char_name: {
                'sentiment_per_sentence': sentiment_scores_per_sentence,
                'aggregated_scores': aggregated_scores
            }
        }
    #text = open('.txt', 'r').read()
    # TODO: Perform sentiment analysis on the text using your chosen tool
    # For example, analyze each sentence or paragraph where entities are identified

    # Save the results to a JSON file
    Book_name = os.path.basename(args.file_path).split('.')[0].replace('_MainCharacters_NER', '')
    json_filename = f'{Book_name}_Sentiment.json'
    save_sentiment_results(results, json_filename )
    # Example filename: 'BookTitle_Sentiment.json'


# Run the main function
if __name__ == "__main__":
    main()