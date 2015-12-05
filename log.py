import sys
from globalvars import COLOR_NAME

LOG_FILE_NAME = 'game.log'
LOG_FILE = None
DO_LOG = True


def init_log():
    global LOG_FILE
    LOG_FILE = open(LOG_FILE_NAME, 'w', encoding = 'utf8') 


def log(str):
    if DO_LOG:
        LOG_FILE.write(str + '\n')
        print(str)


def close_log():
    global LOG_FILE
    LOG_FILE.close()


def str_card(card):
    s = card['name']
    s +=  ' ' + str(card['price'])
    s += '(' + str(card['value']) + ')'
    s += ' ' + COLOR_NAME[card['color']]
    return s


def log_deck(deck):
    log('Start of deck')
    for card in deck: log(str_card(card))
    log('End of deck')


def log_line():
    log('-' * 32)


def log_player(p):
    log(p.name + ' has ' + str(p.money) + ' Gold and ' + str(p.base_score()) + ' Score')
    log(p.name + " hand contains " + str(len(p.hand)) + ' cards')
    log_line()
    for card in p.hand: log(str_card(card))
    log_line()
    log(p.name + " slots contain " + str(len(p.slots)) + ' cards')
    log_line()
    for card in p.slots: log(str_card(card))
    log_line()


def log_full_game_state(gs):
    log('\nGame state on round ' + str(gs.round))
    log('There are ' + str(len(gs.deck)) + ' cards in the deck')
    #log_deck(gs.deck); log('\n')
    for p in gs.players: log_player(p); log('')
    log('Crown owner is player ' + str(gs.crown_owner + 1))
    log('Current is player ' + gs.player().name)
    log('End of game state on round ' + str(gs.round) + '\n')
    
