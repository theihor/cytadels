from actions import *


def action_choose_character(gs, scene, names):
    objects = scene_objects(scene)
    refresh_scene(objects)

    objects = [Drawable(image=window.copy())]
    darking = Drawable(image=Surface(WINDOW_SIZE))
    darking.source_img.set_alpha(200)
    darking.draw_priority = 0
    objects.append(darking)

    cards = []
    for name in names:
        card = ChoiceCard(name, image=CHARACTER_IMAGES[name], size=CARD_SIZE_CHOICE)
        cards.append(card)

    choosing_card_start_animation(cards, objects)

    obj = wait_click(gs, objects)
    choosing_end_animation(cards, drawable=objects)

    return obj.name


def action_choose(gs, scene, names, texts=[]):
    objects = scene_objects(scene)
    refresh_scene(objects)

    objects = [Drawable(image=window.copy())]
    darking = Drawable(image=Surface(WINDOW_SIZE))
    darking.source_img.set_alpha(200)
    darking.draw_priority = 0
    objects.append(darking)

    cards = []
    for i in range(len(names)):
        if i < len(texts):
            text = texts[i]
        card = ChoiceCardWithText(names[i], text, image=Surface(CARD_SIZE_DEFAULT))
        (w, h) = CARD_SIZE_CHOICE
        card.scale(w, h)
        cards.append(card)

    choosing_card_start_animation(cards, objects)

    obj = wait_click(gs, objects)
    choosing_end_animation(cards, drawable=objects)

    return obj.name
    pass


def ability_assassination(gs, scene):
    if gs.player() == gs.human_player():
        victims = [role[0] for role in CHARACTERS if role[0] != 'Assassin']
        choosed = action_choose_character(gs, scene, victims)
        gs.killed = next(c for c in CHARACTERS if c[0] == choosed)
    else:
        gs.killed = random.choice(CHARACTERS[1:])

    m = 'Assassin kills the ' + gs.killed[0] + '!'
    log(m)
    message(m, scene, t=1.5)


def ability_robbery(gs, scene):
    can_rob = [role for role in CHARACTERS if role[0] != 'Assassin' and role[0] != 'Thief' and role[0] != gs.killed[0]]
    if gs.player() == gs.human_player():
        victims = [role[0] for role in can_rob]
        choosed = action_choose_character(gs, scene, victims)
        gs.robbed = next(c for c in CHARACTERS if c[0] == choosed)
    else:
        gs.robbed = random.choice(can_rob)
    m = 'Thief robs the ' + gs.robbed[0] + '!'
    message(m, scene, t=1.5)


def ability_wizardry(gs, scene):
    p = gs.player()
    names = ["Research", "Illusion"]
    texts = ["Discard your hand and tedraw.",
             "Swap your hand with another player."]
    res = action_choose(gs, scene, names, texts)

    if res == "Research":
        n = len(p.hand)
        gs.discard(p.hand)
        p.hand = gs.top_deck(n)
        log(p.roled_name() + ' discards his hand and draws ' + str(n) + ' cards.')
    else:
        victim = random.choice(gs.players)
        hand_ = victim.hand
        p.hand = hand_
        victim.hand = hand_
        log(p.roled_name() + ' swaps his hand with ' + p.name + '.')

    update_hand(gs, scene)
    refresh_scene(scene_objects(scene))
    pass

ABILITY_TAB = {
    'Assassin': ability_assassination,
    'Thief': ability_robbery,
    'Wizard': ability_wizardry
}
