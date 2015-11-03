from globalvars import *
from definitions import *
from log import log
import sys, csv, random
from card import NoImgCard



def load_deck():
    deck = []
    with open(BUILDING_DECK_FILE_NAME, 'r', encoding = 'utf8') as f:
        reader = csv.reader(f, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL, lineterminator='\n')
        for row in reader:
            if row[0] == 'name': continue
            count = int(row[4])
            for i in range(0,count):

                deck.append({'name' : row[0],
                            'price' : int(row[1]),
                            'value' : int(row[2]),
                            'color' : GAME_COLOR[row[3]],
                            'image' : row[5]})
                #print(deck[len(deck) - 1])
        pass
    return deck


def init_hand(game_state):
    hand = game_state.top_deck(4)
    return hand


def init_game():
    deck = load_deck()
    random.shuffle(deck)
    
    game_state = GameState()
    game_state.deck = deck
    
    for i in range(1, COUNT_OF_PLAYERS + 1):
        p = Player("Player " + str(i), i)
        p.hand = init_hand(game_state)
        game_state.players.append(p)
    
    game_state.assign_random_crown_owner()
    return game_state

