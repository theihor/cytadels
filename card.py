from gameobject import *
from loadimg import *


class Card(Updatable):
    def __init__(self):
        Updatable.__init__(self)
        self.source_img = Surface(CARD_SIZE_DEFAULT)
        self.image = self.source_img
        self.rect = self.image.get_rect()
        self.draw_priority = 20
        self.old_rect = None
        self.mouse_over = False

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


class NoImgCard(Card):
    def __init__(self, card_dict):
        Card.__init__(self)
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

        self.source_img = CHARACTER_IMAGES[name]
        self.init_img()

    def init_img(self):
        if self.frame.player.revealed:
            self.source_img = CHARACTER_IMAGES[self.name]
            self.reset_img()
            self.source_img.blit(CARD_TEMPLATE_IMAGE, (0, 0))

            f = pygame.font.Font(GLOBAL_FONT_FILE_NAME, self.rect.h // 12)
            text = f.render(self.name, 1, COLOR_BLACK)
            r = text.get_rect()
            x = self.rect.w // 2 - r.w // 2
            y = self.rect.h * 8 // 10 + 4
            self.source_img.blit(text, (x, y))

            gem = GEM_IMAGES[CHARACTER_GEMS[self.name]]
            x = self.rect.w - gem.get_rect().w - 5
            y = 5
            self.source_img.blit(gem, (x, y))

            text = f.render(str([c[0] for c in CHARACTERS].index(self.name) + 1), 1, COLOR_BLACK)
            r_gem = Rect((x, y), gem.get_rect().size)
            r = text.get_rect()
            x = r_gem.x + (r_gem.w - r.w) // 2
            y = r_gem.y + (r_gem.h - r.h) // 2
            self.source_img.blit(text, (x, y))

            self.reset_img()
        else:
            self.source_img = CARD_BACK_IMAGE
            self.reset_img()
