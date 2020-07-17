import os, random
import data
import re
import pickle

# picks a random word from the words.txt file
def pick_a_word():
    total_bytes = os.stat(data.conf['words_file']).st_size 
    random_point = random.randint(0, total_bytes)

    with open(data.conf['words_file']) as file:
        file.seek(random_point)
        file.readline() # skip this line to clear the partial line
        return file.readline()[:-1] #reads word on this line

# asks the name of the player at beginning of script
def ask_for_name():
    # lets make it basic for now
    return input("So, what's your name ?")

def ask_for_replay():
    answer = input("Will you play again ? (yes or no)")
    
    if answer == "yes":
        return True
    elif answer == "no":
        return False
    else:
        print("Sorry, I didn't get your answer...")
        return ask_for_replay()

def ask_for_letter():
    wrong = True
    letter = ''

    while wrong:
        print("choose a letter :")
        letter = input("")

        try:
            # check if we have only one char
            assert(len(letter) == 1)
            # check if its a letter
            assert re.match( r'[a-z]', letter, re.M|re.I)
        except:
            print("If you don't know what a letter is, choose ONLY ONE amongst those : (a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z)")
            continue
    
        wrong = False
    
    return letter

def has_player_won(hidden_word):
    has_hidden_letters = False
    for letter in hidden_word:
        if letter == '*':
            has_hidden_letters = True
            # no need to keep looping
            break
    
    if has_hidden_letters:
        return False
    else:
        return True

def save_scores(scores):
    with open('scores', 'wb') as file:
        pickler = pickle.Pickler(file)
        pickler.dump(scores)

def load_scores():
    with open('scores', 'rb') as file:
        pickler = pickle.Unpickler(file)
        return pickler.load()