#The official rules of Wordle: https://www.wsj.com/articles/wordle-what-is-word-game-11642016202

#The programs in this repo use the above rules

# wordleV1

-wordle in python (text based)

-interact with a console to play

-requires a python terminal

# wordleV2

-wordle in python (Discord bot)

-interact with a Discord bot to play, within the channel you set the ID for (channelID variable)

-once you start a game, the bot will prompt you for a guess, you enter one, and it will print out the hint, which continues until the game ends

-requires the packages pandas (https://pandas.pydata.org/docs/getting_started/install.html) and discord.py (https://discordpy.readthedocs.io/en/stable/intro.html)

Commands:

#play -- starts a game
#quit -- end current game (counts as a loss)
#stat -- get personal wins, losses, and success rate 
#statall -- get all users wins, losses, and success rates, ranked in descending order by success rate
