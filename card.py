from gameobject import *


class Card(Updatable):
    def __init__(self):
        Updatable.__init__(self)
        self.source_img = Surface(CARD_SIZE_DEFAULT)
        self.image = self.source_img
        self.rect = self.image.get_rect()
        self.draw_priority = 20
        self.old_rect = None
        self.mouse_over = False

        self.mp_on_pick = None

    def on_mouse_over(self):
        if not self.mouse_over:
            self.old_rect = self.rect.copy()
            self.mouse_over = True
        self.draw_priority = 0
        self.reset_img()
        (x, y) = self.pos()
        (w, h) = self.rect.size
        if x + w > WINDOW_SIZE[0]:
            x = WINDOW_SIZE[0] - w
        if y + h > WINDOW_SIZE[1]:
            y = WINDOW_SIZE[1] - h
        self.set_pos(x, y)

    def on_mouse_out(self):
        if self.old_rect and self.mouse_over:
            self.draw_priority = 20
            self.set_rect(self.old_rect.topleft, self.old_rect.size)
            self.old_rect = None
            self.mouse_over = False

    def draw(self, surface):
        if self.mp_on_pick:
            (x, y) = self.pos()
            (mx1, my1) = self.mp_on_pick
            (mx2, my2) = pygame.mouse.get_pos()
            self.mp_on_pick = (mx2, my2)
            self.set_pos(x + (mx2 - mx1), y + (my2 - my1))
        Updatable.draw(self, surface)


class NoImgCard(Card):
    def __init__(self, card_dict):
        Card.__init__(self)
        self.dict = card_dict
        self.name = card_dict['name']
        self.price = card_dict['price']
        self.value = card_dict['value']
        self.color = card_dict['color']
        self.init_img()

    def init_img(self):
        f = pygame.font.Font(GLOBAL_FONT_FILE_NAME, self.rect.h // 10)
        text = f.render(self.name, 1, COLOR_WHITE)
        r = text.get_rect()
        x = self.rect.w // 2 - r.w // 2
        y = self.rect.h * 4 // 10
        self.source_img.blit(text, (x, y))

        text = f.render(str(self.price) + '(' + str(self.value) + ')', 1, COLOR_WHITE)
        x = self.rect.w // 10
        y = self.rect.h // 40
        self.source_img.blit(text, (x, y))

        x = self.rect.w * 8 // 10
        y = self.rect.h // 8
        pygame.draw.circle(self.source_img, COLOR_CODE[COLOR_NAME[self.color]], (x, y), self.rect.h // 10)

        self.reset_img()


class ImgCard(Card):
    def __init__(self, image, card_dict):
        Card.__init__(self)
        self.dict = card_dict
        self.name = card_dict['name']
        self.price = card_dict['price']
        self.value = card_dict['value']
        self.color = card_dict['color']

        self.picture = image
        self.source_img = self.picture
        self.init_img()
        self.image = self.source_img
        self.reset_img()

    def init_img(self):
        self.source_img.blit(CARD_TEMPLATE_IMAGE, (0, 0))

        f = pygame.font.Font(GLOBAL_FONT_FILE_NAME, self.rect.h // 12)
        text = f.render(self.name, 1, COLOR_BLACK)
        r = text.get_rect()
        x = self.rect.w // 2 - r.w // 2
        y = self.rect.h * 8 // 10 + 4
        self.source_img.blit(text, (x, y))

        (x, y) = (20, 20)
        for i in range(self.price):
            self.source_img.blit(COIN_MONEY_IMAGE, (x, y))
            y += COIN_MONEY_IMAGE.get_rect().h + 5
        for i in range(self.value - self.price):
            self.source_img.blit(COIN_VALUE_IMAGE, (x, y))
            y += COIN_VALUE_IMAGE.get_rect().h + 5

        gem = GEM_IMAGES[self.color]
        x = self.rect.w - gem.get_rect().w - 5
        y = 5
        self.source_img.blit(gem, (x, y))

        self.reset_img()


class CharacterCard(Card):
    def __init__(self, name, frame):
        Updatable.__init__(self)
        self.name = name
        self.frame = frame

        self.draw_priority = 25
        self.old_rect = None
        self.mouse_over = False
        self.revealed = False

        self.init_img()
        self.mp_on_pick = None

    def init_img(self):
        if self.name in CHARACTER_IMAGES:
            if self.frame.player.revealed:
                self.source_img = CHARACTER_IMAGES[self.name]
                self.reset_img()
            else:
                self.source_img = CHARACTER_CARD_BACK_IMAGE
                self.reset_img()
        else:
            self.source_img = transparent_surface(PORTRAIT_SIZE)
            self.reset_img()

    def on_mouse_over(self):
        if self.name in CHARACTER_IMAGES and self.frame.player.revealed:
            Card.on_mouse_over(self)


class ChoiceCard(Clickable):
    def __init__(self, name, image=None, size=None):
        Clickable.__init__(self, image=image, size=size)
        (x, y) = CHOICE_DECK_POSITION
        self.set_pos(x, y)
        self.draw_priority = -1
        self.mouse_over = False
        self.name = name

    def on_mouse_over(self):
        if not self.mouse_over:
            self.mouse_over = True

            (x, y) = self.pos()
            (w, h) = self.rect.size

            img = Surface((w + 10, h + 10))
            img.fill(COLOR_GREEN)
            img.blit(self.image, (5, 5))
            self.image = img

            self.set_pos(x - 5, y - 5)

    def on_mouse_out(self):
        if self.mouse_over:
            (x, y) = self.pos()
            self.set_rect((x + 5, y + 5), CARD_SIZE_CHOICE)
            self.mouse_over = False


class CardInHand(Clickable):
    def __init__(self, card):
        self.card = card
        Clickable.__init__(self, image=transparent_surface(self.card.size()))
        self.draw_priority = 10

    def first_click(self):
        (x, y) = pygame.mouse.get_pos()
        self.card.mp_on_pick = (x, y)
        (w, h) = CARD_SIZE_CHOICE
        self.card.scale(w, h)
        x -= self.card.rect.w // 2
        y -= self.card.rect.h // 2
        self.card.set_pos(x, y)

    def second_click(self):
        self.card.mp_on_pick = None

    def collides(self, pos):
        return self.card.collide_rect.collidepoint(pos)

    def draw(self, surface):
        self.card.draw(surface)

    def on_mouse_over(self):
        if not self.card.mp_on_pick:
            self.card.on_mouse_over()

    def on_mouse_out(self):
        if not self.card.mp_on_pick:
            self.card.on_mouse_out()


class ChoiceCardWithText(ChoiceCard):
    def __init__(self, name, text, image=None, size=None):
        ChoiceCard.__init__(self, name, image, size)
        self.name = name
        self.text = text
        self.init_img()

    def init_img(self):
        #self.reset_img()
        self.source_img.blit(CARD_TEMPLATE_IMAGE, (0, 0))

        f = pygame.font.Font(GLOBAL_FONT_FILE_NAME, self.rect.h // 12)
        text = f.render(self.name, 1, COLOR_BLACK)
        r = text.get_rect()
        x = self.rect.w // 2 - r.w // 2
        y = self.rect.h * 8 // 10 + 4
        self.source_img.blit(text, (x, y))

        gem = GEM_IMAGES[0]
        x = self.rect.w - gem.get_rect().w - 5
        y = 5
        self.source_img.blit(gem, (x, y))

        blank = BLANK_IMAGE.copy()
        x = (self.rect.w - blank.get_rect().w) // 2
        y = self.rect.h * 5 // 10
        self.source_img.blit(blank, (x, y))

        f = pygame.font.Font(GLOBAL_FONT_FILE_NAME, 16)
        text = f.render(self.text, 1, COLOR_BLACK)
        self.source_img.blit(text, (x + 4, y + 4))

        self.reset_img()

