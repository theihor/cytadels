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


ABILITY_TAB = {
    'Assassin': ability_assassination,
    'Thief': ability_robbery
}
