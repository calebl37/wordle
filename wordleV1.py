import random
import os

# Loads in a text file, ignoring any lines that start with
# a pound sign '#'.
# In repl.it, this works with path names relative to main.py 
# Files which are in the same folder as main.py need no
# directory prefix.

# Returns the entire filtered text as one string with embedded
# newlines.
def load_text(filename):
  file = open(filename, "r")
  bulk_data = file.read()
  file.close()

  lines = bulk_data.split('\n')
  filtered_lines = []
  for line in lines:
    if not line.startswith('#'):
      filtered_lines.append(line)
  text = '\n'.join(filtered_lines)  
  return text
  

# Takes in a long text and segments it into a list of words.
# This converts all words to lowercase, ignores punctuation and
# line breaks.
def text_to_word_list(text):
  # make all letters lowercase
  text_lower = text.lower()

  # remove all punctuation and new lines.
  text_clean = text_lower.replace("\n", " ")
  text_clean = text_clean.replace(".", "")
  text_clean = text_clean.replace("?", "")
  text_clean = text_clean.replace("!", "")
  text_clean = text_clean.replace(",", " ")
  text_clean = text_clean.replace("-", " ")

  # convert text into a list of individual words.
  word_list = text_clean.split(" ")
  # discard any empty words or words that are all spaces. 
  clean_list = list()
  for word in word_list:
    if word and not word.isspace():
      clean_list.append(word)
  return clean_list


wordle_txt = load_text(os.path.dirname(os.path.realpath(__file__)) + "\\wordleBank.txt")
wordle_list = text_to_word_list(wordle_txt)


def getValidGuess(guessNumber, used):
    valid = False
    while not valid:
        guess = input("Guess " + str(guessNumber) + " - Enter a 5 letter word:\n")
        if len(guess) == 5 and guess in wordle_list and not guess in used:
            valid = True
        else:
            print("Invalid guess, try again\n")
    return guess

#using the offical rules of Wordle, compares _guess_ to _actual_
#and returns a sequence of 5 colored squares based on how close they are
def getHint(actual, guess):
    hintChars = ["B"] * 5
    not_exact_indices = [0,1,2,3,4]
    #check the exact matches 
    for i in range(5):
        if guess[i] == actual[i]:
            hintChars[i] = "G"
            not_exact_indices.remove(i)

    #remove exact matches from the answer 
    actualNoExact = ""
    for j in not_exact_indices:
        actualNoExact += actual[j]

    #check the indirect matches (once the exact matches have been removed)
    for k in not_exact_indices:
        if guess[k] in actualNoExact:
            hintChars[k] = "Y"
            actualNoExact = actualNoExact.replace(guess[k], "", 1)
    hint = ""
    for char in hintChars:
        hint += char
    return  hint + "\n"

def play():

    guessed_words = []

    guesses = 0

    win = False

    wordIndex = random.randint(0,len(wordle_list)-1)

    word = wordle_list[wordIndex]

    while guesses < 6 and not win:
        guess = getValidGuess(guesses + 1, guessed_words)
        print(getHint(word, guess))
        if guess == word:
            win = True
        else:
            guesses += 1
            guessed_words.append(guess)
    if win:
        print("You win!")
    else:
        print("The word was " + word)

play()






