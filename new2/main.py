import time, pygame
from Menu import *
from ResManager import *
from Background import *
#from Transparent import *

SIZE = (1280, 720)
screen = pygame.Surface(SIZE)

class Transparent:
    # Нам нужен спрайт
    # Время за которое появляется спрайт или исчезает
    # Показывать или скрывать спрайт
    def __init__(self, sprite = None, time = 2000, show = True):
        # Получаем копию спрайта, в процессе анимации мы изменяем его
        # и чтобы не изменить оригинал мы получаем копию
        self.sprite = sprite.copy()
        self.sprite.convert_alpha()
        # Устанавливаем флаг для Surface.fill
        if show:
            # Добавление цвета к Surface
            self.flag = pygame.BLEND_RGBA_ADD
        else:
            # Вычитания цвета из Surface
            self.flag = pygame.BLEND_RGBA_SUB

        # Если требуется показывать, то тогда устанавливаем
        # абсолютную прозрачность то есть в 0
        if show:
            self.sprite.fill((0,0,0,255),None,pygame.BLEND_RGBA_SUB)

        # Через какое время требуется изменить прозрачность
        self.time = float(255)/float(time)
        # Это нужно что бы знать запущена ли анимация
        self.run = False
        # Сколько нужно добавить или вычесть альфы из Surface
        self.add = float(0)
        # Нужно что бы посчитать сколько раз мы изменяли альфа канал
        self.count = 0

    # Принимает время с прошлого кадра
    def update(self, dt):
        # Если запущена анимация        
        self.sprite.convert_alpha()
        if self.run:
            # Считаем на сколько нужно изменить значения альфа канала
            self.add += float(dt) * self.time
            # Так как значение цвета число целое, мы должны его ждать
            if int(self.add) > 0:
                # Изменяет альфа канал спрайта
                self.sprite.fill((0,0,0,int(self.add)),None,self.flag)
                # Подсчитываем на сколько он уже изменился
                self.count += int(self.add)
                # Вычитаем целое чтобы не потерять еще не примененные
                # изменения значения прозрачности
                self.add = self.add - int(self.add)
                # Если мы достигли максима изменений (255)
                if self.count > 255:
                    # Сбросим счетчик
                    self.count = 0
                    # Останавливаем анимацию
                    self.run = False

    # Запускаем анимацию
    def start(self):    	
        self.sprite.convert_alpha()
        self.run = True

    # Проверяем запущена ли анимация
    def is_start(self):
        return self.run

    def stop(self):
        self.run = False

    # Меняем флаг для Surface.fill
    def flag_toggle(self):
        if self.flag == pygame.BLEND_RGBA_ADD:
            self.flag = pygame.BLEND_RGBA_SUB
        else:
            self.flag = pygame.BLEND_RGBA_ADD

def get_center(surface, sprite):
    return (surface.w/2 - sprite.w/2,
            surface.h/2 - sprite.h/2 - 50)

# Главный цикл
def loop(screen2,plambir):
    # Создаем класс Clock
    clock = pygame.time.Clock()
    plambir.sprite.convert_alpha()
    # В этой переменной будет сохранятся время прошедшее
    # между рисованием кадров.
    dt = 0
    # Цикл будет работать пока анимация не закончится.
    while plambir.is_start():
        # Это обработка событий, об этом как-нибудь потом.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                plambir.stop()

        screen2.fill((255,255,255))
        # Обновляем анимацию.
        plambir.update(dt)
        # Рисуем
        screen2.blit(plambir.sprite, get_center(screen2.get_rect(), plambir.sprite.get_rect()))
        pygame.display.flip()

        # Здесь указывается максимальное количество кадров в секунду
        # возвращается время прошедшее за время ожидания.
        dt = clock.tick(40)

if __name__ == '__main__':
    pygame.init()

    window = pygame.display.set_mode(SIZE)
    #screen = pygame.display.set_mode(SIZE)

    manager = ResManager()
    pygame.display.set_icon(manager.get_image('icon.png'))
    pygame.display.set_caption("Citadels")    

    citadels = manager.get_image('logo.jpg')
    citadels.convert_alpha()
    window.fill((255,255,255))
    screen.fill((255, 255, 255))

    #screen.blit(citadels, get_center(screen.get_rect(), citadels.get_rect()))
    window.blit(screen, (0, 0))

    plambir = Transparent(citadels, 5000)
    plambir.start()

    loop(window, plambir)

    plambir.flag_toggle()
    plambir.start()

    loop(window, plambir)
    #pygame.display.flip()
    #window.blit(screen, (0, 0))
    
    pygame.key.set_repeat(1, 1)

    items = [(SIZE[0]/2-75, SIZE[1]/2 - 130, u'Play', (0, 0, 0), (7, 16, 45), 0), (SIZE[0]/2-75, SIZE[1]/2-40, u'Quit', (0, 0, 0), (7, 16, 45), 1)]
    game = Menu(items)
    game.menu()

    done = True
    while done:
    	for e in pygame.event.get():
    		if e.type == pygame.QUIT:
    			sys.exit()
    			done = False
    			if done == False:
    				game.menu()
    			if e.key == pygame.K_ESCAPE:
    				game.menu()
    				pygame.key.set_repeat(1,1)
    				done = False

    	BackGround = Background('img/bg_table.png', [0,0])
    	screen.fill([255, 255, 255])
    	screen.blit(BackGround.image, BackGround.rect)
    	window.blit(screen, (0, 0))
    	pygame.display.flip()