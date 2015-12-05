from definitions import *
from animation import *
from globalvars import *
from view import *
import pygame
from log import log

def action_rob(gs, scene):
    objects = []
    for key in scene:
        objects += scene[key]

    robbed = next(p for p in gs.players if p.role == gs.robbed)
    robber = gs.robber()
    frames = scene['frames']
    robbed_frame = next(f for f in frames if f.player.role == robbed.role)
    robber_frame = next(f for f in frames if f.player.role == robber.role)
    (x1, y1) = robbed_frame.global_money_icon_pos()
    (x2, y2) = robber_frame.global_money_icon_pos()
    obj = Drawable(image=MONEY_ICON)
    obj.set_pos(x1, y1)

    m = robbed.money
    robbed.money = 0
    move_animation(obj, (x2, y2), ROBBING_TIME, objects)
    robber.money += m


def action_build(scene, p, card_dict):
    objects = scene_objects(scene)
    card = card_from_dict(card_dict)

    frame = next(f for f in scene['frames'] if f.player == p)

    # spend money
    (x, y) = frame.global_money_icon_pos()
    obj = Drawable(image=MONEY_ICON)
    obj.set_pos(x, y)
    p.money -= card_dict['price']
    move_with_a_animation(obj, (x, -obj.size()[1]), 0.4, objects)

    # play card
    p.hand.remove(card_dict)
    if isinstance(frame, HumanPlayerFrame):
        scene['player_hand'] = [PlayerHand(p.hand)]
        scene['player_hand_cards'] = scene['player_hand'][0].cards
    slot = frame.next_slot()

    (x, y) = frame.global_cards_icon_pos()
    (w, h) = CARDS_ICON.get_rect().size
    card.set_pos(x, y)
    card.scale(w, h)
    open_card_animation(card, slot.card_pos(), slot.card_size(), drawable=objects)

    # set card in slot
    p.slots.append(card_dict)
    frame.put_card_in_slots(card, scene)

    log(p.roled_name() + ' builds ' + str_card(card_dict) + ' and now has ' + str(p.base_score()) + ' Score')


def action_reveal(scene, p):
    objects = scene_objects(scene)
    frame = next(f for f in scene['frames'] if f.player == p)
    p.revealed = True

    card = frame.portrait
    card.init_img()
    frame.adjust_portrait()
    objects.remove(card)

    open_card_animation(card, card.pos(), card.size(), drawable=objects)


def wait_click(gs, objects):
    while True:
        for obj in [obj for obj in objects if isinstance(obj, Updatable)]:
            mp = pygame.mouse.get_pos()
            if obj.collides(mp):
                obj.on_mouse_over()
            else:
                obj.on_mouse_out()
            pass
        refresh_scene(objects)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mp = pygame.mouse.get_pos()
                for obj in [obj for obj in objects if isinstance(obj, Clickable)]:
                    if obj.rect.collidepoint(mp):
                        obj.on_click(gs, objects)
                        return obj


def action_player_chooses_role(role_names, gs, scene):
    p = gs.player()
    role_names.sort(key=lambda x: CHARACTERS_N[x])

    objects = [Drawable(image=window.copy())]
    darking = Drawable(image=Surface(WINDOW_SIZE))
    darking.source_img.set_alpha(200)
    darking.draw_priority = 0
    objects.append(darking)

    cards = []
    for name in role_names:
        card = RoleChoiceCard(name, image=CHARACTER_IMAGES[name], size=CARD_SIZE_CHOICE)
        cards.append(card)

    choosing_start_animation(cards, objects)

    obj = wait_click(gs, objects)

    objects = objects[:1] #scene_objects(scene)
    pos = next(f for f in scene['frames'] if f.player == p).global_portrait_pos()

    move_and_scale_animation(obj, pos, PORTRAIT_SIZE, 0.7, drawable=objects)
    p.role = next(role for role in gs.roles if role[0] == obj.name)
    gs.roles.remove(p.role)


def update_roles(scene):
    scene['portraits'] = []
    frames = scene['frames']
    for frame in frames:
        name = frame.player.role[0]
        frame.portrait = CharacterCard(name, frame)
        frame.adjust_portrait()
        scene['portraits'].append(frame.portrait)


def deck_image(image, n, card_size, stepx=0.2, stepy=0.1):
    cardback = pygame.transform.smoothscale(image, card_size)
    (w, h) = cardback.get_size()
    w += ceil(2 * n * abs(stepx))
    h += ceil(2 * n * abs(stepy))
    surface = transparent_surface((w, h))
    (x, y) = (0, 0)
    if stepx < 0:
        x += (2 * n - 1) * stepx
    if stepy > 0:
        y += (2 * n - 1) * stepy
    whitecard = pygame.transform.smoothscale(CARD_TEMPLATE_IMAGE, CARD_SIZE_DECK)
    for i in range(n * 2):
        if i % 2 == 0 or i == 0 or i == n * 2 - 1:
            surface.blit(cardback, (round(x), round(y)))
        else:
            surface.blit(whitecard, (round(x), round(y)))
        x += stepx
        y -= stepy
    return surface


def choosing_deck_drawable(n):
    img = deck_image(CHARACTER_CARD_BACK_IMAGE, n, CARD_SIZE_CHOICE, stepx=0.4, stepy=0.2)
    deck = Drawable(image=img)
    (x, y) = CHOICE_DECK_POSITION
    deck.set_pos(x, y)
    deck.draw_priority = 0
    return deck


def action_role_choosing(gs, scene):
    scene['portraits'] = []
    objects = scene_objects(scene)
    deck = choosing_deck_drawable(len(gs.roles))
    objects.append(deck)
    refresh_scene(objects)

    while gs.current_player < COUNT_OF_PLAYERS:
        p = gs.player()
        log(p.name + ' is choosing a character from')
        log(str([role[0] for role in gs.roles]))
        if p == gs.human_player():
            action_player_chooses_role([role[0] for role in gs.roles], gs, scene)
        else:
            card = Drawable(image=CHARACTER_CARD_BACK_IMAGE, size=CARD_SIZE_CHOICE)
            (x, y) = CHOICE_DECK_POSITION
            card.set_pos(x, y)
            pos = next(f for f in scene['frames'] if f.player == p).global_portrait_pos()

            move_and_scale_animation(card, pos, PORTRAIT_SIZE, 0.5, objects)
            p.role = random.choice(gs.roles)
            gs.roles.remove(p.role)

        log(p.name + ' have choosed a ' + p.role[0])
        p.revealed = False
        gs.inc_player()
        update_roles(scene)
        objects = scene_objects(scene)
        deck = choosing_deck_drawable(len(gs.roles))
        objects.append(deck)
        #refresh_scene(objects)

    #deck = choosing_deck_drawable(len(gs.roles) - 1)
    move_with_a_animation(deck, (-deck.size()[0], deck.pos()[1]), 0.5, drawable=objects)






