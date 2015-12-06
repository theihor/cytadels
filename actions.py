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
    move_with_a_animation(obj, scene['coins'][0].center_pos(), 0.4, objects)

    p.hand.remove(card_dict)
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
    refresh_scene(objects)


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
    #print([obj for obj in objects if isinstance(obj, Clickable)])
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
                    if obj.collides(mp):
                        obj.on_click(gs, objects)
                        return obj


def action_player_chooses_role(role_names, gs, scene):
    p = gs.player()
    role_names.sort(key=lambda x: CHARACTERS_N[x])
    objects = scene_objects(scene)
    refresh_scene(objects)

    objects = [Drawable(image=window.copy())]
    darking = Drawable(image=Surface(WINDOW_SIZE))
    darking.source_img.set_alpha(200)
    darking.draw_priority = 0
    objects.append(darking)

    cards = []
    for name in role_names:
        card = ChoiceCard(name, image=CHARACTER_IMAGES[name], size=CARD_SIZE_CHOICE)
        cards.append(card)

    choosing_start_animation(cards, objects)

    obj = wait_click(gs, objects)

    objects = objects[:1] #scene_objects(scene)
    pos = next(f for f in scene['frames'] if f.player == p).global_portrait_pos()

    move_and_scale_animation(obj, pos, PLAYER_PORTRAIT_SIZE, 0.7, drawable=objects)
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


def choosing_deck_drawable(n):
    img = deck_image(CHARACTER_CARD_BACK_IMAGE, n, CARD_SIZE_CHOICE, stepx=0.4, stepy=0.2)
    deck = Drawable(image=img)
    (x, y) = CHOICE_DECK_POSITION
    deck.set_pos(x, y)
    deck.draw_priority = 0
    return deck


def action_role_choosing(gs, scene):
    objects = scene_objects(scene)
    refresh_scene(objects)
    end_round_animation(scene['portraits'], objects)

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

    move_with_a_animation(deck, (-deck.size()[0], deck.pos()[1]), 0.5, drawable=objects)


def update_hand(gs, scene):
    player_hand = PlayerHand(gs.human_player().hand)
    scene['player_hand'] = [player_hand]
    scene['player_hand_cards'] = player_hand.cards


def action_player_builds(obj, gs, scene):
    objects = scene_objects(scene)
    card_dict = obj.card.dict
    card = obj.card
    objects.append(card)
    p = gs.human_player()
    frame = next(f for f in scene['frames'] if f.player == p)

    # spend money
    (x, y) = frame.global_money_icon_pos()
    coin = Drawable(image=MONEY_ICON)
    coin.set_pos(x, y)
    p.money -= card_dict['price']
    move_with_a_animation(coin, scene['coins'][0].center_pos(), 0.4, objects)

    slot = frame.next_slot()

    move_and_scale_animation(card, slot.card_pos(), slot.card_size(), drawable=objects)

    # set card in slot
    p.slots.append(card_dict)
    card = card_from_dict(card_dict)
    frame.put_card_in_slots(card, scene)

    log(p.roled_name() + ' builds ' + str_card(card_dict) + ' and now has ' + str(p.base_score()) + ' Score')
    refresh_scene(objects)


def action_player_picked_card(obj, gs, scene):
    d = next(d for d in gs.human_player().hand if d['name'] == obj.card.name)
    gs.human_player().hand.remove(d)

    update_hand(gs, scene)
    objects = scene_objects(scene)
    refresh_scene(objects)
    objects = [Drawable(image=window.copy()), obj]
    obj.first_click()

    (w, h) = WINDOW_SIZE
    fy = HUMAN_PLAYER_FRAME_POS[1]
    hy = HAND_POSITION[1]
    sh = MAIN_SLOT_IMAGE.get_rect().h
    h1 = ((fy + sh) + hy) // 2
    build_area = Clickable(size=(w, h1))
    build_area.draw_priority = 1
    objects.append(build_area)

    undo_area = Clickable(size=(w, h - h1))
    undo_area.set_pos(0, h1)
    undo_area.draw_priority = 1
    objects.append(undo_area)

    area = wait_click(gs, objects)
    if area == undo_area or not gs.human_player().can_build(obj.card.dict):
        obj.second_click()
        gs.human_player().hand.append(obj.card.dict)
        update_hand(gs, scene)
        return False
    else:
        obj.second_click()
        update_hand(gs, scene)
        action_player_builds(obj, gs, scene)
        return True


def action_take_money(p, scene):
    objects = scene_objects(scene)
    frame = next(f for f in scene['frames'] if f.player == p)
    (x, y) = scene['coins'][0].center_pos()
    obj = Drawable(image=MONEY_ICON)
    obj.set_pos(x, y)
    move_with_a_animation(obj, frame.global_money_icon_pos(), 0.4, objects)
    p.money += 2
    refresh_scene(objects)


def action_human_player_takes_card(p, gs, scene):
    objects = scene_objects(scene)
    refresh_scene(objects)

    objects = [Drawable(image=window.copy())]
    darking = Drawable(image=Surface(WINDOW_SIZE))
    darking.source_img.set_alpha(200)
    darking.draw_priority = 0
    objects.append(darking)

    dicts = gs.top_deck(2)
    log(p.roled_name() + ' draws ' + str_card(dicts[0]) + ' and ' + str_card(dicts[1]))

    cards = []
    for dict in dicts:
        card = card_from_dict(dict)
        card = ChoiceCard(dict['name'], image=card.source_img, size=CARD_SIZE_DECK)
        (x, y) = DECK_POSITION
        card.set_pos(x, y)
        cards.append(card)

    choosing_card_start_animation(cards, objects)

    obj = wait_click(gs, objects)
    dict = next(d for d in dicts if d['name'] == obj.name)
    dicts.remove(dict)
    gs.discarded += dicts

    player_hand = scene['player_hand'][0]

    objects = objects[:1]
    move_and_scale_animation(obj, player_hand.next_card_pos(), CARD_SIZE_HAND, 0.5, objects)

    p.hand.append(dict)
    log(p.roled_name() + ' keeps ' + str_card(dict) + ' and now has ' + str(len(p.hand)) + ' cards.')
    update_hand(gs, scene)


def action_take_card(p, gs, scene):
    objects = scene_objects(scene)
    refresh_scene(objects)

    dicts = gs.top_deck(2)
    log(p.roled_name() + ' draws ' + str_card(dicts[0]) + ' and ' + str_card(dicts[1]))

    cards = []
    for _ in dicts:
        card = Drawable(image=CARD_BACK_IMAGE, size=CARD_SIZE_DECK)
        (x, y) = DECK_POSITION
        card.set_pos(x, y)
        card.draw_priority = 0
        cards.append(card)

    choosing_card_start_animation(cards, objects)
    idle()

    dict = random.choice(dicts)
    dicts.remove(dict)
    gs.discarded += dicts

    frame = next(f for f in scene['frames'] if f.player == p)
    card = random.choice(cards)
    objects.remove(card)
    cards.remove(card)
    move_and_scale_animation(cards[0],
                             frame.global_cards_icon_pos(),
                             CARDS_ICON.get_rect().size, 0.4, objects)

    p.hand.append(dict)
    log(p.roled_name() + ' keeps ' + str_card(dict) + ' and now has ' + str(len(p.hand)) + ' cards.')
    refresh_scene(objects)


def action_human_player_turn(gs, scene):
    objects = scene_objects(scene)
    p = gs.human_player()

    used_action = False
    used_ability = True

    build_count = 1
    if p.role[0] == 'Architect':
        build_count = 3

    while not(used_action and used_ability and build_count <= 0):
        obj = wait_click(gs, objects)
        #print(obj)
        if isinstance(obj, CardInHand) and build_count > 0:
            built = action_player_picked_card(obj, gs, scene)
            if built: build_count -= 1

        if isinstance(obj, Coins) and not used_action:
            action_take_money(p, scene)
            used_action = True

        if isinstance(obj, Deck) and not used_action:
            action_human_player_takes_card(p, gs, scene)
            used_action = True

        if not p.card_to_build():
            build_count = 0

        objects = scene_objects(scene)
        refresh_scene(objects)






