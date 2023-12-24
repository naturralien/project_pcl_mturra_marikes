##############################################################################################################
##############################################################################################################
##### DO NOT MODIFY THIS CODE #####
# This code is to be used as is.

import os
import sys

# Markers for the start and end of Project Gutenberg headers/footers
TEXT_START_MARKERS = frozenset((
    "*END*THE SMALL PRINT",
    "*** START OF THE PROJECT GUTENBERG",
    "*** START OF THIS PROJECT GUTENBERG",
    "This etext was prepared by",
    "E-text prepared by",
    "Produced by",
    "Distributed Proofreading Team",
    "Proofreading Team at http://www.pgdp.net",
    "http://gallica.bnf.fr)",
    "      http://archive.org/details/",
    "http://www.pgdp.net",
    "by The Internet Archive)",
    "by The Internet Archive/Canadian Libraries",
    "by The Internet Archive/American Libraries",
    "public domain material from the Internet Archive",
    "Internet Archive)",
    "Internet Archive/Canadian Libraries",
    "Internet Archive/American Libraries",
    "material from the Google Print project",
    "*END THE SMALL PRINT",
    "***START OF THE PROJECT GUTENBERG",
    "This etext was produced by",
    "*** START OF THE COPYRIGHTED",
    "The Project Gutenberg",
    "http://gutenberg.spiegel.de/ erreichbar.",
    "Project Runeberg publishes",
    "Beginning of this Project Gutenberg",
    "Project Gutenberg Online Distributed",
    "Gutenberg Online Distributed",
    "the Project Gutenberg Online Distributed",
    "Project Gutenberg TEI",
    "This eBook was prepared by",
    "http://gutenberg2000.de erreichbar.",
    "This Etext was prepared by",
    "This Project Gutenberg Etext was prepared by",
    "Gutenberg Distributed Proofreaders",
    "Project Gutenberg Distributed Proofreaders",
    "the Project Gutenberg Online Distributed Proofreading Team",
    "**The Project Gutenberg",
    "*SMALL PRINT!",
    "More information about this book is at the top of this file.",
    "tells you about restrictions in how the file may be used.",
    "l'authorization à les utilizer pour preparer ce texte.",
    "of the etext through OCR.",
    "*****These eBooks Were Prepared By Thousands of Volunteers!*****",
    "We need your donations more than ever!",
    " *** START OF THIS PROJECT GUTENBERG",
    "****     SMALL PRINT!",
    '["Small Print" V.',
    '      (http://www.ibiblio.org/gutenberg/',
    'and the Project Gutenberg Online Distributed Proofreading Team',
    'Mary Meehan, and the Project Gutenberg Online Distributed Proofreading',
    '                this Project Gutenberg edition.',
))


TEXT_END_MARKERS = frozenset((
    "*** END OF THE PROJECT GUTENBERG",
    "*** END OF THIS PROJECT GUTENBERG",
    "***END OF THE PROJECT GUTENBERG",
    "End of the Project Gutenberg",
    "End of The Project Gutenberg",
    "Ende dieses Project Gutenberg",
    "by Project Gutenberg",
    "End of Project Gutenberg",
    "End of this Project Gutenberg",
    "Ende dieses Projekt Gutenberg",
    "        ***END OF THE PROJECT GUTENBERG",
    "*** END OF THE COPYRIGHTED",
    "End of this is COPYRIGHTED",
    "Ende dieses Etextes ",
    "Ende dieses Project Gutenber",
    "Ende diese Project Gutenberg",
    "**This is a COPYRIGHTED Project Gutenberg Etext, Details Above**",
    "Fin de Project Gutenberg",
    "The Project Gutenberg Etext of ",
    "Ce document fut presente en lecture",
    "Ce document fut présenté en lecture",
    "More information about this book is at the top of this file.",
    "We need your donations more than ever!",
    "END OF PROJECT GUTENBERG",
    " End of the Project Gutenberg",
    " *** END OF THIS PROJECT GUTENBERG",
))


LEGALESE_START_MARKERS = frozenset(("<<THIS ELECTRONIC VERSION OF",))


LEGALESE_END_MARKERS = frozenset(("SERVICE THAT CHARGES FOR DOWNLOAD",))

def strip_headers(text):
    """Remove lines that are part of the Project Gutenberg header or footer."""
    lines = text.splitlines()
    sep = str(os.linesep)

    out = []
    i = 0
    footer_found = False
    ignore_section = False

    for line in lines:
        reset = False

        # Header removal
        if i <= 600 and any(line.startswith(token) for token in TEXT_START_MARKERS):
            reset = True

        if reset:
            out = []
            continue

        # Footer detection
        if i >= 100 and any(line.startswith(token) for token in TEXT_END_MARKERS):
            footer_found = True

        if footer_found:
            break

        # Legalese removal
        if any(line.startswith(token) for token in LEGALESE_START_MARKERS):
            ignore_section = True
            continue
        elif any(line.startswith(token) for token in LEGALESE_END_MARKERS):
            ignore_section = False
            continue

        if not ignore_section:
            out.append(line.rstrip(sep))
            i += 1

    return sep.join(out)

##############################################################################################################
##############################################################################################################

#### MODIFY HERE ####
import re

def write_chapter_to_file(chapter_name:str, chapter_text:str,book_title:str):
    """
    Create folder with book title and create a subfolder for chapters, in which    
    txt files for all chapters are created
    """
    #replace whitespace with underscore in chapter name
    chapter_name = chapter_name.replace(" ","_")
    #create directory if it doesnt already exist
    if not os.path.exists(f"{book_title}/chapters"):
        os.makedirs(f"{book_title}/chapters")
    #write text of chapter to file
    with open(f"{book_title}/chapters/{chapter_name}.txt","w",encoding="utf8") as file:
        file.writelines(chapter_text)
        

def get_chapter_list_of_book(book_lines: list[str], chapter_markers: tuple[str], content_headers: tuple[str], book_title: str) -> dict():
    """
    Creates dictionary from book text split into list of strings at newline. 
    
    Returned dictionary includes name of chapter as key and index as value.
    
    Params: 
    book_lines: book split at linebreak as list of strings
    chapter_markers: Substrings included in chapter names (e.g. "Chapter") as tuple
    content_headers: Names of content list headers (e.g. "CONTENT") as tuple    
    book_title: title of book as string
    """
    #set variable to check if content list header was found
    content_list_found = False
    #map chapters of Jekyll and Hyde
    chapter_name_index_map = dict()
    #iterate through text segments
    for i in range(len(book_lines)):
        #check if current segment is header of content list
        if not content_list_found and book_lines[i] in content_headers:
            #set contentlist bool to True and continue with next iteration
            content_list_found = True
            continue
        #check if content list has been found
        if(content_list_found):
            #remove superflous text from chapters with existing chapter markers 
            book_lines[i] = book_lines[i].split(".")[0] if book_lines[i].startswith(chapter_markers) else book_lines[i]
            #check if either chapter marker appears in current segment or Jekyll special condition is met
            if book_lines[i].startswith(chapter_markers) or (book_title == "DrJekyllAndMrHyde" and re.match("^[A-Z .'’]+$",book_lines[i])):
                #break loop if first chapter name reappears as we have looped through the entire content list
                if (book_lines[i] in chapter_name_index_map):
                    break
                #add chapter to chapter list
                chapter_name_index_map[book_lines[i]] = len(chapter_name_index_map)
    #return chapter name index dict
    return chapter_name_index_map 

def split_book_by_chapter(cleaned_text:str, book_title:str):
    """
    Implement a function that splits the book into chapters and saves 
    each chapter in a separate file in a folder named after the book title.
    """
    # Add your code here to split the cleaned_text into chapters
    #splits text at linebreak
    segments = cleaned_text.split("\r\n")
    #define tuple of chapter titles
    chapter_markers = ("Letter", "Chapter", "CHAPTER")
    #define list of content list headers
    content_headers = ("CONTENTS", "Contents")
    #call function to get chapter list
    chapter_list = get_chapter_list_of_book(segments,chapter_markers, content_headers, book_title)

    #chapter indexer because past mattia decided to rewrite the function and now we need to index the chapters the first time to prevent the content list from being identified as chapters 
    chapter_indexer = []

    #iterate through book
    for i in range(len(segments)):
        #identify chapter markers
        if segments[i] in chapter_list:
            #check if indexer does not contain chapter marker 
            if segments[i] not in chapter_indexer:
                #add chapter to indexer
                chapter_indexer.append(segments[i])
            else:
                #add chapter limit marker for splitting
                segments[i] = "[CHAPTER_LIMIT]" + segments[i]

    #rejoin text with chapter limit markers
    cleaned_text_with_chapter_limits = "\r\n".join(segments)
    #divide text by chapter limit markers
    chapters = cleaned_text_with_chapter_limits.split("[CHAPTER_LIMIT]")
    #remove the first entry, so the introductive pages are not in the chapters list  
    chapters.pop(0)
    #write each chapter to a seperate file
    for chapter_name, index in chapter_list.items():
        #call function to write chapter to file 
        write_chapter_to_file(f"Chapter {index + 1}", chapters[index], book_title)
    return

def create_book_folder(path: str, bookname: str) -> str:
    """
    Function that takes a path and a bookname as arguments and creates a folder named after the bookname
    """
    # takes path from first command line argument
    if len(path) < 1:
        path = sys.argv[0]
    # ensures that path ends with a backslash
    path_folder = path + "\\" + bookname
    #create folder if it doesnt already exist
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)
    return path_folder


def write_whole_text_to_file(text: str, path: str):
    """
    Function that takes a text and a path as arguments and writes it to a file called content.txt
    """
    # strip linebreaks from text
    #text_without_linebreaks = text.replace("\r\n", "")
    # write text to file content.txt
    file_path = os.path.join(path, "content.txt")

    # check if file exists, can be deleted later
    print(f'Writing to {file_path}')

    # write text to file
    f= open(file_path,"w",encoding="utf8")
    #f.write(text_without_linebreaks)
    f.write(text)
    

    # check if file was written, can be deleted later
    print(f'Finished writing to {file_path}')
    f.close() # close file

def main():
    #IMPORTANT: file path of text file in folder Books needs to be passed as an argument
    # insures that there are two command line arguments if not the program exits
    if len(sys.argv) != 2:
        print("Usage: python gutenberg_cleanup.py <path_to_book_file>")
        sys.exit(1)

    # takes the file path from the command line arguments
    file_path = sys.argv[1]

    # extracts the book title from the file name
    book_title = os.path.basename(file_path).replace('.txt', '')

    # 1. Read the text file
    with open(file_path, encoding="utf8") as f:
        lines = f.readlines()
    # 2. Clean the text
    booktext = strip_headers("".join([w.lstrip() for w in lines]))
    # 3. Save the cleaned text in the book title folder
    book_folder_path = create_book_folder(os.path.dirname(os.path.abspath(__file__)), book_title)
    write_whole_text_to_file(booktext, book_folder_path)
    # 4. Split the text into chapters and save them in the book title folder under a subfolder named 'chapters'
    split_book_by_chapter(booktext, book_title)

if __name__ == '__main__':
    main()