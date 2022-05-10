import discord
import time
from discord.ext import commands
import random
import pandas as pd

#The id for this bot - it is a secret, so you can either make your own or contact me for the token to use mine.
TOKEN = ""

#change this to the ID of the server channel you want this bot to operate in
channelID = 813984299644747787

#the hashtag will be used to distinguish commands for this bot
bot = commands.Bot(command_prefix = "#")


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

#initializing the word bank
wordle_txt = load_text("wordleBank.txt")
wordle_list = text_to_word_list(wordle_txt)

class Player:

    """
    A class used to represent an user who plays at least one game of Wordle

    ...

    Attributes
    ----------
    name : str
        the discord username of this player
    wins : int
        the number of Wordle victories achieved by this player
    losses : int
        the number of Wordle losses suffered by this player
    answer : str
        the 5 letter solution for this player's current game of Wordle
    guesses : int
        the number of incorrect guesses so far in this player's current game of Wordle
    guessed: list of str
        the words this player has already guessed in the current game of wordle
    
    """

    def __init__(self, name, wins, losses):
        """
        Parameters
        ----------
        name : str
            the discord username of this player
        wins : int
            the number of Wordle victories achieved by this player
        losses : int
            the number of Wordle losses suffered by this player
        """

        self.name = name
        self.wins = wins
        self.losses = losses
        self.answer = None
        self.guesses = 0
        self.guessed = []

    #Inputs: none
    #Outputs: none
    #retrieves a random 5 letter word from the wordle word bank
    #sets that as the answer for this player's current game
    def setAnswer(self):
        wordIndex = random.randint(0,len(wordle_list)-1)
        self.answer = wordle_list[wordIndex]
        print(self.answer)
    
    #Inputs: none
    #Outputs: str
    #observer for this player's discord username
    def getName(self):
        return self.name
    
    #Inputs: none
    #Outputs: str
    #observer for the 5 letter answer in this player's current game
    def getAnswer(self):
        return self.answer

    #Inputs: str
    #Ouputs: boolean
    #has this player already guessed _word_ in their current game?
    def hasGuessed(self, word):
        return word in self.guessed

    #Inputs: none
    #Outputs: none
    #adds a guess to this player
    def incrementGuesses(self):
        self.guesses +=1 
    
    #Inputs: str
    #Outputs: none
    #adds _word_ to this player's list of previously gussed words in their current game
    def addToGuessed(self, word):
        self.guessed.append(word)

    #Inputs: boolean
    #Outputs: none
    #increments either the win count or loss count for this player, depending on whether _has_won is True or False
    def updateStats(self, hasWon):
        if hasWon:
            self.wins +=1
        else:
            self.losses +=1

    #Inputs: none
    #Outputs: none
    #Erases current game stats for this player, but does not erase long-term infomartion (name, wins, losses)
    def reset(self):
        self.guesses = 0
        self.guessed = []
        self.answer = None

    #Inputs: none
    #Outputs: str
    #Formats a string for the bot prompt on this player's next guess
    def getPrompt(self):
        return self.name + " guess " + str(self.guesses+1) + ": enter a 5 letter word"

    #Inputs: none
    #Outputs: str
    #Formats a string for this player's info that will be added to the log
    def summarize(self):
        return self.name + " " + str(self.wins) + " " + str(self.losses)

    #Inputs: none
    #Outputs: boolean
    #Is this player out of guesses in their current game?
    def outOfGuesses(self):
        return self.guesses == 6

    #Inputs: none
    #Outputs: str
    #Formats a string for this player's info that will be used in the stat command,
    #which is wins, losses, and success rate
    def getStats(self):
        ratio = round(self.wins / (self.wins + self.losses) * 100, 2)
        return "Stats for " + self.name + ": \nWins: " + str(self.wins) + "\nLosses: " + str(self.losses) + "\nSuccess rate: " + str(ratio) + "%"


#from the given _path_ to the log, returns a list of player objects whose name, wins and losses
#are based on the information in the log (a text file)

#the log is of the format:
#<user_1_name> <wins> <losses> /n
#<user_2_name> <wins> <losses> /n
#<user_3_name> <wins> <losses> /n
#...
#<user_n_name> <wins> <losses> /n
def load_existing_data(path):
    #convert the text file to one string
    user_info = []
    log = open(path, "r")
    bulk_data = log.read()
    log.close()
    #split the string by newlines, such that each line contains information about one user
    lines = bulk_data.split('\n')
    #discard the last line, which is just a newline by default
    lines = lines[:-1]
    #iteratively generate a player object from each line
    for line in lines:
        #based on the log format above, converts the line to a playr object, using
        #name, wins and losses in the constructor
        playerData = line.split(" ")
        name, wins, losses = playerData[0], int(playerData[1]), int(playerData[2])
        user_info.append(Player(name, wins, losses))
    return user_info

#intializes all player objects based on the log, which stores game records even while offline
user_info = load_existing_data("wordlelog.txt")

#only one user can play a game of Wordle at a time. This pointer tracks who that user is
whoPlaying = None

#overwrites the log with updated player stats
def updateLog():
    with open("wordlelog.txt", 'w') as file:
        for playerObj in user_info:
            file.write(playerObj.summarize() + "\n")

#given a Discord username, retrieves the corresponding player object, None if it does not exist
def getPlayerObject(username):
    for playerObj in user_info:
        if playerObj.getName() == username:
            return playerObj
    return None

#using the offical rules of Wordle, compares _guess_ to _actual_
#and returns a sequence of 5 colored squares based on how close they are
def getHint(actual, guess):
    hintChars = ["⬜"] * 5
    not_exact_indices = [0,1,2,3,4]
    #check the exact matches 
    for i in range(5):
        if guess[i] == actual[i]:
            hintChars[i] = "🟩"
            not_exact_indices.remove(i)

    #remove exact matches from the answer 
    actualNoExact = ""
    for j in not_exact_indices:
        actualNoExact += actual[j]

    #check the indirect matches (once the exact matches have been removed)
    for k in not_exact_indices:
        if guess[k] in actualNoExact:
            hintChars[k] = "🟨"
            actualNoExact = actualNoExact.replace(guess[k], "", 1)
    hint = ""
    for char in hintChars:
        hint += char
    return  hint + "\n"

#startup function to verify that the bot is online in the server
@bot.event
async def on_ready():
    print(str(bot.user.name) +  " has connected to Discord!")
    await bot.change_presence(activity=discord.Game(name="wordle"))


#play command - used to start a game of Wordle
@bot.command(name = "play")
async def play(ctx):
    global whoPlaying 
    #this command can only be called in the channel specified above
    if ctx.channel.id == channelID:

        #retrieves the player object associated with the user who called this command
        current_user = getPlayerObject(ctx.author.name)

        #if the user has never played before, they do not have a player object, so a new one
        #must be created 
        if current_user is None:
            current_user = Player(ctx.author.name, 0, 0)
            user_info.append(current_user)

        #if the user has played before (they do have a player object), then their game is
        #restarted, updating the player object accordingly
        else:
            current_user.reset()

        #generates the random 5 letter answer for this game, for this user
        current_user.setAnswer()
        await ctx.send(current_user.getPrompt())
        #set the global tracker for who is currently playing
        whoPlaying = current_user.getName()

#stat command - prints individual stats for the user who invoked this command
#(wins, losses, and success rate)
@bot.command(name = "stat")
async def stat(ctx):
    #this command can only be called in the channel specified above
    if ctx.channel.id == channelID:
        current_user = getPlayerObject(ctx.author.name)
        if current_user is None:
            await ctx.send(ctx.author.name + " has not played any wordle yet")
        else:
            await ctx.send(current_user.getStats())

#statall command - uses tabular data to print the stats of all players (wins, losses, and success rate)
#ranked in descending order by success rate
@bot.command(name = "statall")
async def stat(ctx):
    #this command can only be called in the channel specified above
    if ctx.channel.id == channelID:

        #iteratively convert all player objects into an nx4 array, for n users, 
        #each with values for the categories "name", "wins", "losses", "success rate"
        tabular = []
        for playerObj in user_info:
            data = playerObj.summarize().split(" ")
            w, l = int(data[1]), int(data[2])
            if w + l != 0:
                ratio = w / (w + l)
                data.append(ratio)
                tabular.append(data)

        #use a pandas dataframe to house all player data
        df = pd.DataFrame(tabular, columns=["Name", "Wins", "Losses", "Success Rate"])

        #sorting the table in descending order of success rate
        df = df.sort_values(by=['Success Rate'], ascending=False, ignore_index=True)
        df.index = list(range(1, len(tabular)+1))
        await ctx.send(df)

        
#quit command
@bot.command(name = "quit")
async def stat(ctx):
    global whoPlaying
    #this command can only be called in the channel specified above
    if ctx.channel.id == channelID:
        current_user = getPlayerObject(ctx.author.name)
        if current_user is not None:
            answer = current_user.getAnswer()
            await ctx.send(current_user.getName() + ", the answer was " + answer)
            whoPlaying = None
            current_user.updateStats(False)
            updateLog()
            

#response to a given message        
@bot.event
async def on_message(message):
    global user_info
    global whoPlaying

    #to prevent this bot from interacting with itself
    if message.author == bot.user or message.author.bot:
        return

    #so the bot can send it back in the same channel
    channel = bot.get_channel(message.channel.id)

    who = message.author.name


    #clean up message
    guess = message.content.lower()

    #message is command
    if guess.startswith("#"):
        await bot.process_commands(message)

    #message is a guess
    else:

        #message is not a guess, so exit 
        if len(guess) > 5:
            return

        #retrieve player object based on the author name on the message
        current_user = getPlayerObject(who)

        #enforcing the rules that only one person can play at a time and games must be played in the specified channel
        if current_user is None or not current_user.getName() == whoPlaying or message.channel.id != channelID:
            return

        answer = current_user.getAnswer()

        #valid guess
        if len(guess) == 5 and guess in wordle_list and not current_user.hasGuessed(guess):
            await channel.send(getHint(answer, guess))
        
        #invalid guess
        else:
            await channel.send(current_user.getName() + ", invalid guess, try again")
            return

        #guess is incorrect
        if guess != answer:
            current_user.incrementGuesses()
            current_user.addToGuessed(guess)

            #user is out of guesses
            if current_user.outOfGuesses():
                await channel.send(current_user.getName() + ", the answer was " + answer)
                whoPlaying = None
                current_user.updateStats(False)
                updateLog()
            #user still has guesses remaining
            else:
                time.sleep(1)
                await channel.send(current_user.getPrompt())
        
        #guess is correct
        else:
            await channel.send(current_user.getName() + ", you win!")
            whoPlaying = None
            current_user.updateStats(True)
            updateLog()

#runs the bot using the given token     
bot.run(TOKEN)






