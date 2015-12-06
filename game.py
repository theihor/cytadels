from log import *
from characters import *
import game_init
from actions import *
from abilities import *


def p_build(scene, p):
    card = p.card_to_build()
    if card and len(p.slots) < COUNT_OF_SLOTS:
        action_build(scene, p, card)
    idle()


def p_act(p, gs, scene):
    if random.random() <= len(p.hand) / 4.5:
        action_take_money(p, scene)
    else:
        action_take_card(p, gs, scene)
    idle()


def p_use_ability(p, gs, scene):
    if p.role[0] in ABILITY_TAB:
        ABILITY_TAB[p.role[0]](gs, scene)
    else:
        p.role[1](p, gs)


def do_turn(gs, scene):
    p = gs.player()
    action_reveal(scene, p)

    if p.role[0] == 'King':
        log(p.roled_name() + ' gets the crown!')
        gs.crown_owner = gs.players.index(p)

    if p == gs.human_player():
        action_human_player_turn(gs, scene)
        p_use_ability(p, gs, scene)
        return

    if p.role == gs.killed: 
        log(p.roled_name() + ' is killed and skips his turn!')
        return
    if p.role == gs.robbed:
        robber = next(p for p in gs.players if p.role[0] == 'Thief')
        action_rob(gs, scene)
        log(p.roled_name() + ' is robbed by ' + robber.roled_name() + '!')

        
    if random.random() <= 0.99:
        play_role = random.randint(0, 2)
        if play_role == 0:
            p_use_ability(p, gs, scene)
            p_act(p, gs, scene)
            p_build(scene, p)
        elif play_role == 1:
            p_act(p, gs, scene)
            p_use_ability(p, gs, scene)
            p_build(scene, p)
        elif play_role == 2:
            p_act(p, gs, scene)
            p_build(scene, p)
            p_use_ability(p, gs, scene)
    else:
        log(p.roled_name() + ' is not using his ability.')
        p.act_random(gs)
        p_build(scene, p)
        
    if p.role[0] == 'Architect':
        p_build(scene, p)
        p_build(scene, p)
pass


def init_round(gs, scene):
    gs.round += 1
    gs.new_round()
    log('Round ' + str(gs.round))
    gs.current_player = 0
    gs.choosing_stage = True
    action_role_choosing(gs, scene)
    gs.choosing_stage = False
    gs.current_player = 0


def next_turn(gs, scene):
    objects = scene_objects(scene)
    log('Turn of ' + CHARACTERS[gs.current_player][0])
    show_message('Turn of ' + CHARACTERS[gs.current_player][0], drawable=objects)

    p = gs.player()
    if p:
        log(p.name + ' is ' + CHARACTERS[gs.current_player][0])
        do_turn(gs, scene)
    else:
        log('There is no ' + CHARACTERS[gs.current_player][0] + '.')
    gs.inc_player()


def run_round(gs):
    init_round()
    while gs.current_player < len(CHARACTERS):
        next_turn(gs)
pass

    
    
def run_game():
    init_log()

    game_state = game_init.init_game()
    log_full_game_state(game_state)
    while not game_state.end():
        run_round(game_state)
        #log_full_game_state(game_state)
    pass
    log_full_game_state(game_state)

    winner = game_state.winner().name
    log(game_state.winner().name + " WINS THE GAME!")

    close_log()
    return (game_state, winner)
    
#run_game()