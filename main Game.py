import pygame
import sys
from random import randint


def base():
    # setup
    pygame.init()
    clock = pygame.time.Clock()
    frame = 0

    # game screen
    screen = pygame.display.set_mode((960, 960))  # задали окно
    pygame.display.set_caption("Underground menace")  # Задали заголовок
    screen.fill((202, 220, 159))
    pygame.display.flip()

    # MC sprite class
    class MC(pygame.sprite.Sprite):
        def __init__(self):  # Создание спрайта
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/MC.png")  # создание изображение
            self.rect = self.image.get_rect()  # создание прямоугольника для манипуляции с изображением
            self.rect.centerx = 480  # Положение прямоугольника
            self.rect.centery = 480
            self.speedx = 0  # начальная скорость
            self.lastkey = 0

            self.coordright = self.rect.right
            self.coordleft = self.rect.left
            self.coordtop = self.rect.top
            self.coordbottom = self.rect.bottom
            self.coordcenterx = self.rect.centerx
            self.coordcentery = self.rect.centery

        # Движение
        def update(self):
            self.speedx = 0

            if keystate[pygame.K_a]:
                self.lastkey = 1
                if (frame // 10) % 2 == 0:
                    self.image = pygame.image.load("pictures/MC turn left1.png")
                else:
                    self.image = pygame.image.load("pictures/MC turn left2.png")
                self.speedx = -playerspeed
                self.rect.x += self.speedx

            if keystate[pygame.K_d]:
                self.lastkey = 2
                if (frame // 10) % 2 == 0:
                    self.image = pygame.image.load("pictures/MC turn right1.png")
                else:
                    self.image = pygame.image.load("pictures/MC turn right2.png")
                self.speedx = playerspeed
                self.rect.x += self.speedx

            if keystate[pygame.K_s]:
                self.lastkey = 3
                if (frame // 10) % 2 == 0:
                    self.image = pygame.image.load("pictures/MC walk1.png")
                else:
                    self.image = pygame.image.load("pictures/MC walk2.png")
                self.speedy = playerspeed
                self.rect.y += self.speedy

            if keystate[pygame.K_w]:
                self.lastkey = 4
                if (frame // 10) % 2 == 0:
                    self.image = pygame.image.load("pictures/MC turn back1.png")
                else:
                    self.image = pygame.image.load("pictures/MC turn back2.png")
                self.speedy = -playerspeed
                self.rect.y += self.speedy

            # Спрайт направления
            if not (keystate[pygame.K_w]) and not (keystate[pygame.K_s]) and not (keystate[pygame.K_a]) and not (
                    keystate[pygame.K_d]):
                if self.lastkey == 1:
                    self.image = pygame.image.load("pictures/MC turn left.png")
                if self.lastkey == 2:
                    self.image = pygame.image.load("pictures/MC turn right.png")
                if self.lastkey == 3:
                    self.image = pygame.image.load("pictures/MC.png")
                if self.lastkey == 4:
                    self.image = pygame.image.load("pictures/MC back.png")

            # screen limits
            if self.rect.right > 960:
                self.rect.right = 960
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > 960:
                self.rect.bottom = 960
            if self.rect.top < 0:
                self.rect.top = 0


    class Shoot(pygame.sprite.Sprite):
        def __init__(self):  # Создание спрайта
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/projectright1.png")  # создание изображение
            self.rect = self.image.get_rect()  # создание прямоугольника для манипуляции с изображением
            self.rect.centerx =500
            self.rect.centery = 500
            self.speedx = 0
            self.speedy = 0

        def update (self):
            self.speedx = projectspeedy
            self.rect.x += self.speedx
            self.speedy = projectspeedx
            self.rect.y += self.speedy





    class Enemy(pygame.sprite.Sprite):
        def __init__(self, MC):  # Создание спрайта
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/troop1.png")  # создание изображение
            self.rect = self.image.get_rect()  # создание прямоугольника для манипуляции с изображением
            self.rect.left = 0  # Положение прямоугольника
            self.rect.centery = 360
            self.speedx = 0

        def update(self):
            self.speedx = enemyspeed
            self.rect.x += self.speedx
            if (frame // 10) % 2 == 0:
                self.image = pygame.image.load("pictures/troop1.png")
            else:
                self.image = pygame.image.load("pictures/troop2.png")

    level1 = ["@@@@@##@@@@@",
              "@##########@",
              "@##########@",
              "@##########@",
              "@##########@",
              "############",
              "############",
              "@##########@",
              "@##########@",
              "@##########@",
              "@##########@",
              "@@@@@##@@@@@", ]

    def levelmaker(level):
        collis = []

        for i, line in enumerate(level):
            for j, character in enumerate(line):
                if character == "@":
                    s = randint(2, 4)
                    if s == 2:
                        texture = pygame.image.load("pictures/Wall2.png")
                    if s == 3:
                        texture = pygame.image.load("pictures/Wall3.png")
                    if s == 4:
                        texture = pygame.image.load("pictures/Wall4.png")
                    block = pygame.Rect(i * 80, j * 80, 80, 80)
                    collis.append((block, texture))
        return collis

    collis = levelmaker(level1)

    # Инициализация спрайта
    mc_group = pygame.sprite.Group()  # создание группы для отрисовки спрайта
    enemy_group = pygame.sprite.Group()
    shoot_group = pygame.sprite.Group()
    mc = MC()  # Создание спрайта
    shoot = Shoot()
    enemy = Enemy(MC)
    mc_group.add(mc)
    shoot_group.add(shoot)
    enemy_group.add(enemy)

    while True:  # логика окна
        clock.tick(60)
        if frame > 60:
            frame = 0
        frame = frame + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # закрытие окна

            # diagonal speed control
            enemyspeed = 5
            playerspeed = 5
            projectspeedx = 10
            projectspeedy = 10
            playerspeedmem = playerspeed
            keystate = pygame.key.get_pressed()
            if (keystate[pygame.K_a] and keystate[pygame.K_w]) or (
                    keystate[pygame.K_a] and keystate[pygame.K_s]) or (
                    keystate[pygame.K_d] and keystate[pygame.K_w]) or (
                    keystate[pygame.K_d] and keystate[pygame.K_s]):
                playerspeed = playerspeed / 1.5
            else:
                playerspeed = playerspeedmem
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    new_shoot = Shoot()
                    shoot_group.add(new_shoot)

        shoot_group.update()
        mc_group.update()
        enemy_group.update()

        screen.fill((202, 220, 159))

        for rect in collis:
            screen.blit(rect[1], rect[0])

        shoot_group.draw(screen)
        mc_group.draw(screen)  # прорисовка спрайта
        enemy_group.draw(screen)
        pygame.display.flip()  # обновление окна


base()
