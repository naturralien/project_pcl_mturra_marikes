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
        #sentiment_results = book_text.affect_frequencies
        if analyzer == 'emotion':
            sentiment_results = book_text.raw_emotion_scores
            #sentiment_results = [book_text.raw_emotion_scores(sentence) for sentence in book_text.sentences]
        elif analyzer == 'emotion_intensity':
            sentiment_results = book_text.affect_intensity
            #sentiment_results = [book_text.affect_intensity(sentence) for sentence in book_text.sentences]
        elif analyzer == 'top_emotions':
            sentiment_results = book_text.top_emotions
            #sentiment_results = [book_text.top_emotions(sentence) for sentence in book_text.sentences]
    # using the default analyzer for sentiment analysis
    else:
        sentiment_results = book_text.affect_frequencies
        #sentiment_results = [book_text.affect_frequencies(sentence) for sentence in book_text.sentences]
        #print(sentiment_results)
    # returns the sentiment results and the analyzer used
    return sentiment_results, analyzer


# Function to save sentiment analysis results to a JSON file
def save_sentiment_results(results, filename):
    # TODO: Save the sentiment analysis results in a structured JSON format
    with open(filename, 'w') as output_file:
        json.dump(results, output_file, cls='utf-8', indent=2)
    pass


# Main function
def main():

    # TODO: Load or define the text for analysis
    #text = "I hate you" #"Your text for sentiment analysis."
    parser = argparse.ArgumentParser(description='Perform sentiment analysis on given txt file.')
    parser.add_argument('file_path', help='Path to txt file to be analyzed.')
    args = parser.parse_args()
    try:
        #with open(args.file_path, 'r', encoding='utf-8') as file:
        #    text = file.read()

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
        for occurrence in main_character.Occurrences:
            #occurrence_per_chapter[occurrence.chapter] = occurrence_per_chapter.get(occurrence.chapter, 0) + 1
            #chapter_key = occurrence.chapter[0]
            # converting it to tuple because list is not hashable
            chapter_key = tuple(occurrence.chapter)
            occurrence_per_chapter[chapter_key] = occurrence_per_chapter.get(chapter_key, 0) + 1

            # Analyze the sentiment of the sentence
            sentence_sentiments, _ = analyze_sentiment(occurrence.sentence)
            sentiment_scores_per_sentence[f'Chapter {chapter_key}: Sentence {occurrence.sentence}'] = sentence_sentiments
            # Print the results of sentiment analysis of each sentence
            #for i, result in enumerate(sentence_sentiments):
            #    print(f' Sentence {i+1} sentiment for {char_name}: {result}') #in chapter {chapter_key}: {result}'

            #idk what this is for
            #for i, (emotion, score) in enumerate(sentence_sentiments.items()):
                #print(f'Chapter {chapter_key}: Sentence {i+1} sentiment ({emotion}): {score}')
            # for easier reading

            print()
        """ 
        not necessary maybe:   
        print(f'{char_name} appears in the following chapters:')
        for chapter_key, count in occurrence_per_chapter.items():
            print(f'Chapter {chapter_key}: {count} occurrences')
        """
        """"
            if chapter_key in occurrence_per_chapter:
                occurrence_per_chapter[chapter_key] += 1
            else:
                occurrence_per_chapter[chapter_key] = 1
        print(f'{char_name} appears in the following chapters:')
        """
        print(f' The sentiment scores associated with {char_name} are:')
        for sentence_key, sentiment_scores in sentiment_scores_per_sentence.items():
            print(f' Sentence {sentence_key}: {sentiment_scores}')
            print()
    #text = open('.txt', 'r').read()
    # TODO: Perform sentiment analysis on the text using your chosen tool
    # For example, analyze each sentence or paragraph where entities are identified

    #sentiment_results = analyze_sentiment(text)
    #print(sentiment_results)

    # Save the results to a JSON file
    save_sentiment_results(sentiment_results, 'BookTitle_Sentiment.json')
    # Example filename: 'BookTitle_Sentiment.json'


# Run the main function
if __name__ == "__main__":
    main()
