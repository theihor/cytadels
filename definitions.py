from globalvars import COUNT_OF_PLAYERS
from log import *
import random
from characters import *


class Player:
    def __init__(self, name, id):
        self.id = 0
        self.name = name
        self.money = 2
        self.slots = []
        self.hand = []
        self.revealed = False
    pass

    role = ('Noone', noone)

    def act_random(self, gs):
        #print(random.random(), ' <= ' ,len(self.hand) / 5.0)
        if random.random() <= len(self.hand) / 4.5:
            self.money += 2
            log(self.roled_name() + ' takes 2 Gold and now has ' + str(self.money) + ' Gold')
        else:
            cards = gs.top_deck(2)
            log(self.roled_name() + ' draws ' + str_card(cards[0]) + ' and ' + str_card(cards[1]))
            card = random.choice(cards)
            cards.remove(card)
            gs.discarded += cards
            self.hand.append(card)
            log(self.roled_name() + ' keeps ' + str_card(card) + ' and now has ' + str(len(self.hand)) + ' cards.')
    pass

    def card_to_build(self):
        can_build = [card for card in self.hand if card['price'] <= self.money and not card in self.slots]
        if can_build:
            return random.choice(can_build)

    def build_random(self, gs):
        can_build = [card for card in self.hand if card['price'] <= self.money and not card in self.slots]
        if can_build:
            card = random.choice(can_build)
            self.money -= card['price']
            self.hand.remove(card)
            self.slots.append(card)
            
            log(self.roled_name() + ' builds ' + str_card(card) + ' and now has ' + str(self.base_score()) + ' Score')
        pass
    pass
    
    def base_score(self):
        s = 0
        for card in self.slots: s += card['value']

        colors = set([card['color'] for card in self.slots])
        if not (BONUS_COLORS - colors): s += 3
     
        return s
    pass
    
    def roled_name(self):
        return self.role[0] + ' (' + self.name + '[' + str(self.money) + ' ' + str(self.base_score()) + '])' 
pass


class GameState:
    the_deck = []

    def __init__(self):
        self.players = []
        self.deck = []
        self.discarded = []
        self.current_player = 0
        self.crown_owner = 0
        self.round = 0
        self.killed = ('Noone', noone)
        self.robbed = ('Noone', noone)
        self.roles = CHARACTERS[:]
        random.shuffle(self.roles)
        self.choosing_stage = True
    pass

    def set_the_deck(self, deck):
        self.the_deck = deck

    def new_round(self):
        self.killed = ('Noone', noone)
        self.robbed = ('Noone', noone)
        self.roles = CHARACTERS[:]
        random.shuffle(self.roles)
        self.choosing_stage = True
    
    def refresh_deck(self):
        if self.discarded:
            self.deck = self.discarded
            random.shuffle(self.deck)
            self.discarded = []
        else:
            self.deck = self.the_deck.copy()
    
    def discard(self, cards):
        self.discarded += cards
    
    def top_deck(self, n = 1):
        #log('n = ' + str(n) + ' deck = ' + str(len(self.deck)) + ' discarded = ' + str(len(self.discarded)) + ' in game = ' + str(sum(len(p.hand) + len(p.slots) for p in self.players)))
    
        i = 0; res = []
        
        while i < n:
            if not self.deck: 
              #  if not self.discarded: return res 
                self.refresh_deck()
            card = self.deck.pop()
            res.append(card)
            i += 1
        return res
    pass
    
    def inc_player(self):
        self.current_player += 1
        #if self.choosing_stage:
        #    if self.current_player == COUNT_OF_PLAYERS:
        #        self.current_player = 0
        #else:
        #    if self.current_player == len(CHARACTERS):
        #        self.current_player = 0
        #pass
        
    def player(self):
        if self.choosing_stage:
            return self.players[(self.crown_owner + self.current_player) % COUNT_OF_PLAYERS ]
        else:
            return next((p for p in self.players if p.role[0] == CHARACTERS[self.current_player][0]), None)
            
    def winner(self):
        #base = [p.base_score() for p in self.players]
        
        #full = [p for p in self.players if len(player.slors) == 8]
        

        
        return max(self.players, key=lambda p: p.base_score())
 
    def end(self):
        return next((True for p in self.players if len(p.slots) == 8), False)
        
    def assign_random_crown_owner(self):
        self.crown_owner = random.randint(0, COUNT_OF_PLAYERS - 1)

    def human_player(self):
        return self.players[0]

    def robber(self):
        return next(p for p in self.players if p.role[0] == 'Thief')

    def human_turn(self):
        p = self.player()
        if p: return p == self.human_player()
