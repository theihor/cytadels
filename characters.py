from log import log, str_card
from globals import *
import random

def noone(self, gs):
    log(self.name + ' is Noone and does nothing.')
    return gs

def assassin(self, gs):
    gs.killed = random.choice(CHARACTERS[1:])
    log(self.roled_name() + ' kills the ' + gs.killed[0] + '!')
    
def thief(self, gs):
    can_rob = [role for role in CHARACTERS if role[0] != 'Assassin' and role[0] != 'Thief' and role[0] != gs.killed[0]]
    gs.robbed = random.choice(can_rob)
    log(self.roled_name() + ' robs the ' + gs.robbed[0] + '!')
    
def wizard(self, gs):
    if bool(random.getrandbits(1)):
        n = len(self.hand)
        gs.discard(self.hand)
        self.hand = gs.top_deck(n)
        log(self.roled_name() + ' discards his hand and draws ' + str(n) + ' cards.')
    else:
        p = random.choice(gs.players)
        hand = p.hand
        p.hand = self.hand
        self.hand = hand
        log(self.roled_name() + ' swaps his hand with ' + p.name + '.')
pass

def king(self, gs):
    gold = sum(1 if card['color'] == GAME_COLOR['YELLOW'] else 0 for card in self.slots)
    self.money += gold
    log(self.roled_name() + ' collects ' + str(gold) + ' Gold from Yellow cards.')
    
def bishop(self, gs):
    gold = sum(1 if card['color'] == GAME_COLOR['BLUE'] else 0 for card in self.slots)
    self.money += gold
    log(self.roled_name() + ' collects ' + str(gold) + ' Gold from Blue cards.')
    
def merchant(self, gs):
    gold = sum(1 if card['color'] == GAME_COLOR['GREEN'] else 0 for card in self.slots)
    self.money += gold + 1
    log(self.roled_name() + ' collects ' + str(gold) + ' Gold from Green cards.')
    log(self.roled_name() + ' collects 1 Gold because he is Merchant.')
    
def architect(self, gs):
    self.hand += gs.top_deck(2)
    log(self.roled_name() + ' draws 2 cards.')
    
def warlord(self, gs):
    gold = sum(1 if card['color'] == GAME_COLOR['RED'] else 0 for card in self.slots)
    self.money += gold
    log(self.roled_name() + ' collects ' + str(gold) + ' Gold from Red cards.')
    
    can_annoy = [p for p in gs.players if p.role[0] != 'Bishop']
    p = random.choice(can_annoy)
    can_ruin = [card for card in p.slots if card['price'] - 1 <= self.money]
    if can_ruin:
        card = random.choice(can_ruin)
        p.slots.remove(card)
        gs.discarded.append(card)
        self.money -= card['price'] - 1
        log(self.roled_name() + ' ruins ' + str_card(card) + ' of ' + p.roled_name() + '.')
pass

CHARACTERS = [ 
  ('Assassin', assassin), 
  ('Thief', thief),
  ('Wizard', wizard ),
  ('King', king), 
  ('Bishop', bishop),
  ('Merchant', merchant),
  ('Architect', architect),
  ('Warlord', warlord)]
