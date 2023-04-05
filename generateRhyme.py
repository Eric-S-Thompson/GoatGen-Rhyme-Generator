import pronouncing
import random

class GenerateRhyme:
    data = [""]
    def __init__(self, data):
        self.data = data
        print("Initialized!")

    # Returns a random title between 1 and 5 words long
    def randomTitle(self):
        title = ""
        numWords = random.randint(1, 5)
        for x in range(numWords): # Loop and add numWords words to the title
            possible = []
            while not possible:  # Make sure there are choices, not an empty line
                possible = self.chooseRandom().split()
            word = random.choice(possible)  # Pick one word from the sentence
            title += word.capitalize()
            title += " "
        return title

    # Returns the last word of a passed in line
    def getLastWord(self, line):
        words = list(line.split(" "))
        wordsLength = len(words)
        return words[wordsLength-1]

    # Returns list of rhymes for the last word of a given line
    def getRhymes(self, line):
        lastWord = self.getLastWord(line)
        return pronouncing.rhymes(lastWord)

    # Searches for lines in our data which end with a rhyme
    def getRhymesEnding(self, rhymes, completeRhyme):
        candidates = []
        #Iterate every combination of last words and rhymes
        for string in self.data:
            lowString = self.getLastWord(string).lower()
            for rhyme in rhymes:
                if(rhyme == lowString):
                    if not(string in candidates): #Not a repeat
                        if not(string in completeRhyme):
                            candidates.append(string)
        return candidates

    # Searches for lines in our data containing a rhyme at any point
    def getRhymesGeneral(self, rhymes, completeRhyme):
        candidates = []
        # Iterate every combination of lines and rhymes
        for string in self.data:
            lowString = string.lower()
            for rhyme in rhymes:
                #if re.search(r'\b' + re.escape(rhyme) + r'\b', string):
                if (rhyme) in lowString:
                    if not (string in candidates): #Not a repeat
                        if not (string in completeRhyme):
                            candidates.append(string)
        return candidates

    # Creates a rhyme dictionary based on scheme
    # First entry is based on provided first line
    # For every unique character in the scheme a rhyme list is created, and added to the dict
    # character  = key
    # rhyme list = value
    def createRhymeDictionary(self, scheme, firstLine):
        duplicatesRemoved = []
        for character in scheme:  # Removing duplicate characters
            if character not in duplicatesRemoved:
                duplicatesRemoved.append(character)

        # Dictionary of key value pairs, and a duplicate list for easy searching/comparison reasons
        rhymeDict = {}
        rhymeList = []
        first = True
        # Generate a rhyme list for each unique character in the rhyme scheme
        for character in duplicatesRemoved:
            if first:  # First element is based on provided first line
                tempList = self.getRhymes(firstLine)
                while not tempList:  # Empty list, get a random one
                    print("No initial rhymes found! Generating...")
                    tempList = self.getRhymes(random.choice(self.data))
                rhymeDict[character] = tempList
                rhymeList.append(tempList)
                first = False
            else:
                tempList = self.getRhymes(random.choice(self.data))

                done = False
                while not done:  # Check that list isn't empty or a duplicate
                    while not tempList:  # Empty list, get a random one
                        tempList = self.getRhymes(random.choice(self.data))
                    for r in rhymeList:  # Check if first or last element matches any in the rhymeList
                        if r[0] == tempList[0] or r[-1] == tempList[-1]:
                            tempList = self.getRhymes(random.choice(self.data))
                        else:
                            done = True

                rhymeDict[character] = tempList
                rhymeList.append(tempList)
        return rhymeDict

    # Chooses random line from all the data
    def chooseRandom(self):
        return random.choice(self.data)

    # Creates rhyme based on a scheme
    # Loops through each character of the scheme and consults generated rhyme dictionary to find next line
    # Uses firstLine as a starting point
    # Treats character 'X' as a random line
    def createRhymeWithScheme(self, scheme, firstLine):
        scheme = scheme.upper()
        completeRhyme = firstLine + '\n'
        previous = self.getRhymes(firstLine)
        rhymeDict = self.createRhymeDictionary(scheme, firstLine)

        for c in scheme[1:]:
            if c == 'X':  # Random lyric
                chosen = self.chooseRandom()
                completeRhyme += chosen + '\n'
            else:
                # Sentences ending in a rhyme
                possible = self.getRhymesEnding(rhymeDict[c], completeRhyme)
                if possible:    # Found sentence ending in rhyme
                    chosen = random.choice(possible)
                else:           # Could not find sentence ending in rhyme
                    possible = self.getRhymesGeneral(rhymeDict[c], completeRhyme)   # Look for general rhyme
                    if not possible:    # No general rhyme, treat as X
                        print("Couldn't find another rhyme for " + c + ": picking a random lyric...")
                        chosen = self.chooseRandom()
                        rhymeDict[c] = self.getRhymes(chosen)
                    else:
                        chosen = random.choice(possible)
                completeRhyme += chosen + '\n'  # Append
        # Print our final result
        print("=======================================================")
        print("The Mountain Goats' newest song: " + self.randomTitle())
        print("=======================================================")
        print(completeRhyme)

    # Generates a rhyming song from a given set of possible lines, then prints the result
    # numLines - The length of our generated song
    # firstLine - Initially provided line to build from
    # data - list of strings, each one being a potential line to choose from
    def createRhyme(self, numLines, firstLine):
        completeRhyme = firstLine + '\n'
        count = 0

        previous = self.getRhymes(firstLine)

        # Loop through and generate each line
        while (count < numLines):
            rhymesList = self.getRhymes(firstLine)
            chosen = ""

            # Sentences ending in a rhyme
            possible = self.getRhymesEnding(rhymesList, completeRhyme)
            if possible:
                chosen = random.choice(possible)
                completeRhyme += chosen + '\n'
                count += 1

            # Sentences containing a rhyme
            possible = self.getRhymesGeneral(rhymesList, completeRhyme)
            if not possible:
                print("Retrying...")
                possible = self.getRhymesEnding(previous, completeRhyme)
                if possible:
                    chosen = random.choice(possible)
                    completeRhyme += chosen + '\n'
                    count += 1
                else:
                    print("No more rhymes found, picking a random line")   # Can't continue from here, dead end
                    chosen = self.chooseRandom()
            else:
                chosen = random.choice(possible)
                completeRhyme += chosen + '\n'
                count += 1

            # Update the line we're working off of
            previous = rhymesList
            firstLine = chosen
        # Print our final result
        print("=======================================================")
        print("The Mountain Goats' newest song: " + self.randomTitle())
        print("=======================================================")
        print(completeRhyme)