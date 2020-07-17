import data
import functions as f
import random
import pickle
from pathlib import Path

# first say hello
def main():
    hello = "Hello, welcome to our Knowledge game"
    print(hello)
    name = f.ask_for_name()
    scores = {}


    # check if player has local scores
    # first check if file exists
    score_file = Path("scores")
    if score_file.is_file():
        # file exists, open it
        scores = f.load_scores()
    else:
        # create an empty file, and save empty dictionary to it
        scores = {}
        f.save_scores(scores)

    # check if player has scores
    if name in scores.keys():
        wlc_bck = "Welcome back {name} ! It's nice to see you again :)".format(name=name) 
        print(wlc_bck)
        by_the_way = "By the way, your total score so far is {} : way to go !".format(scores[name]) 
        print(by_the_way)
    else:
        scores[name] = 0
        got_it = "got it {name}, nice to meet you ! I'm Champa. I will save you in my database so that I will remember you next time :) just type your name in next time you start this script.".format(name=name)
        print(got_it)


    # loop for the game
    wanna_play = True
    while wanna_play:
        print("So you want to play eh ? Ok i'll pick a word for you...")

        print("bzzzzzzzzzzzzzzzzzzzz...")
        tries_left = data.conf['max_tries']
        random_word = f.pick_a_word()

        # build hidden version
        hidden_word = "".join(['*' for letter in random_word])

        print("TNNNNG !!")
        
        print("Ok so, You have {tries_left} tries to find the word I'm thinking about.".format(tries_left=tries_left))

        # loop for turns left
        while tries_left > 0:
            print(hidden_word)

            player_letter = f.ask_for_letter()
            tries_left = tries_left - 1

            # now, check if letter provided by player is a hit or a miss
            i=0 # cursor
            letters_found = 0
            # for each letter in word
            for letter in random_word:
                # if we havn't found this letter yet, display it
                if player_letter == letter and hidden_word[i] == '*':
                    hidden_word = list(hidden_word)
                    hidden_word[i] = letter
                    ''.join(hidden_word)
                    letters_found = letters_found + 1
                # if we have already found this letter, set letters_found as -1 for later error
                elif player_letter == letter and hidden_word[i] != '*':
                    letters_found = -1
                i = i + 1
            # end for each letter loop

            if letters_found == -1:
                print("hey, you have already found this letter ! don't go wasting your turns ! Let's say this one doesn't count...")
                tries_left = tries_left + 1
            elif letters_found > 0:
                print("Yay ! The hidden word has {nb} letter '{letter}'".format(nb=letters_found, letter=player_letter))
                tries_left = tries_left + 1

                if f.has_player_won(hidden_word):
                    break
            else:
                print("Too bad, the hidden word has no '{letter}' so you havn't found any new letters this time.".format(letter=player_letter))

            print("you have {tries_left} turns left".format(tries_left=tries_left))
        # end turn loop

        if f.has_player_won(hidden_word):
            print("Congrats {name}! The word I was thinking about was {hidden_word}".format(name=name, hidden_word=hidden_word))
            sum = len(hidden_word) + tries_left
            print("You get 1 point for finding each letter of this word, and 1 point for each turn you had left ({letters_found} + {tries_left} = {sum} points)".format(letters_found=len(hidden_word), tries_left=tries_left, sum=sum))
            print("I'm saving this to your global score.")
            scores[name] = scores[name] + sum
            f.save_scores(scores)
            print("You can play again later and start with your score, just enter the same name next time !")
        else:
            print("Looks like I won this time ! You didn't earn any point, but don't worry you can play again !")

        print("your total score is {}".format(scores[name]))
        wanna_play = f.ask_for_replay()
    # end game loop

    print("see you {} !".format(name))


main()