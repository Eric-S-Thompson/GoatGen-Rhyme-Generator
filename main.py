import os
import sys
import time

import lyricsgenius
import re

import ASCIIPrinter
import generateRhyme

GENIUS_ACCESS_TOKEN = 'no token' # Paste your token into /lyrics/token.txt if you want to generate your own lyric files

# Loads lyrics (from genius) into a text file
def load_lyrics(filename, artistName, numSongs):
    file = open(filename, "w", errors='ignore')

    genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN,
    skip_non_songs=True, excluded_terms=["(Remix)", ("Live")], remove_section_headers=True)

    #Search top # songs for the artist
    artist = genius.search_artist(artistName, max_songs=numSongs)

    #Store in array
    songs = artist.songs

    #Loop through every song and write them to file after removing unwanted info
    for song in songs:
        temp = song.lyrics
        tempNameGone = temp.split('\n', 1)[1] #Remove first line (title)
        tempNameGone = re.sub(r'(You might also like)*\d*(Embed)', '', tempNameGone) #Remove "You might also like" and "##Embed" at the end of each lyric
        tempNameGone += '\n\n\n' #Add some spacing between different songs
        file.write(tempNameGone)
    file.close()

# Prompts to begin the webscraper
def webScrapePrompt():
    print("IMPORTANT: You must have your own Genius access token to access the API used for gathering the lyrics. Paste the token code into /lyrics/token.txt")
    if(os.path.isfile('lyrics/token.txt')):
        file = open('lyrics/token.txt')
        data = file.read()
        print("token: " + data)
        global GENIUS_ACCESS_TOKEN
        GENIUS_ACCESS_TOKEN = data
    else:
        print("token.txt not found. ")
        return
    fileToCreate = 'lyrics/' + input("Enter the name of the file to be created ")
    artistName = input("Enter the name of the artist to search for ")
    numLines = int(input("Enter the number of songs to scrape at most "))
    load_lyrics(fileToCreate, artistName, numLines)
    return fileToCreate

# Prompts for opening files, retries until the user selects or creates a valid file
def fileOpenPrompt():
    fileToOpen = 'lyrics/' + input("Enter the file name to open ")
    while (not os.path.isfile(fileToOpen)):
        userInput = input("File does not exist! Enter again, or type 'add' to create new file ")
        if (userInput == 'add'):
            fileToOpen = webScrapePrompt()
        else:
            fileToOpen = 'lyrics/' + input("Enter the file name to open ")
    return fileToOpen

# Prompts for generating rhymes
def rhymePrompt():
    startLine = ""
    choice = input("Rhyme Scheme mode or Normal? ('1' or '2') ")
    while True:
        startLine = input("Enter the initial line (or 'exit' to quit) ")
        if (startLine == "exit"):
            break
        if (choice == '1'):
            scheme = input("Enter rhyme scheme ('X' for random line, otherwise use any letter) ")
            rhymeMaker.createRhymeWithScheme(scheme, startLine)
        else:
            numLines = int(input("How many lines (roughly) should it generate? "))
            rhymeMaker.createRhyme(numLines, startLine)

if __name__ == '__main__':

    #load_lyrics('test', 'The Mountain Goats', 3)
    fileToOpen = fileOpenPrompt()
    print("Opening file " + fileToOpen + "...")
    file = open(fileToOpen, "r")
    print("Reading in file...")
    data = file.read()
    print("Splitting file into separate lines...")
    lines = data.splitlines()

    print("Initializing rhyme maker...")
    printer = ASCIIPrinter.ASCIIPrint()
    printer.printASCII(1)
    printer.printASCII(2)
    rhymeMaker = generateRhyme.GenerateRhyme(lines)

    rhymePrompt()

    file.close()
    printer.printASCII(-1)
    print("Thank you for using GoatGen!")
    sys.exit("All gone!")