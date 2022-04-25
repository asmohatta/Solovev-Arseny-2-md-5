import pygame
import sys
from random import randint


def base():

    pygame.init()
    clock = pygame.time.Clock()
    frame = 0
    spawnpos = 0
    screen = pygame.display.set_mode((960, 960))
    pygame.display.set_caption("Underground menace")
    screen.fill((202, 220, 159))
    pygame.display.flip()

    class MC(pygame.sprite.Sprite): # Класс главного героя
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/MC.png")
            self.rect = self.image.get_rect()
            self.rect.centerx = 480
            self.rect.centery = 200
            self.speedx = 0
            self.speedy = 0
            self.lastkey = 0

        def update(self):

            # Движение и коллизии
            self.speedx = 0
            self.speedy = 0
            if keystate[pygame.K_a]:
                self.lastkey = 1
                if (frame // 10) % 2 == 0:
                    self.image = pygame.image.load("pictures/MC turn left1.png")
                else:
                    self.image = pygame.image.load("pictures/MC turn left2.png")
                self.speedx = -playerspeed
                self.rect.x += self.speedx
                for block in collis:
                    block = block[0]
                    if self.rect.colliderect(block):
                        self.rect.left = block.right
            if keystate[pygame.K_d]:
                self.lastkey = 2
                if (frame // 10) % 2 == 0:
                    self.image = pygame.image.load("pictures/MC turn right1.png")
                else:
                    self.image = pygame.image.load("pictures/MC turn right2.png")
                self.speedx = playerspeed
                self.rect.x += self.speedx
                for block in collis:
                    block = block[0]
                    if self.rect.colliderect(block):
                        self.rect.right = block.left
            if keystate[pygame.K_s]:
                self.lastkey = 3
                if (frame // 10) % 2 == 0:
                    self.image = pygame.image.load("pictures/MC walk1.png")
                else:
                    self.image = pygame.image.load("pictures/MC walk2.png")
                self.speedy = playerspeed
                self.rect.y += self.speedy
                for block in collis:
                    block = block[0]
                    if self.rect.colliderect(block):
                        self.rect.bottom = block.top
            if keystate[pygame.K_w]:
                self.lastkey = 4
                if (frame // 10) % 2 == 0:
                    self.image = pygame.image.load("pictures/MC turn back1.png")
                else:
                    self.image = pygame.image.load("pictures/MC turn back2.png")
                self.speedy = -playerspeed
                self.rect.y += self.speedy
                for block in collis:
                    block = block[0]
                    if self.rect.colliderect(block):
                        self.rect.top = block.bottom

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


            # Границы экрана
            if self.rect.right > 960:
                self.rect.right = 960
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > 960:
                self.rect.bottom = 960
            if self.rect.top < 0:
                self.rect.top = 0

        # Функция стрельбы
        def shoot(self):
            fireball = Fireball(self.rect.centerx, self.rect.centery, projectspeedx, projectspeedy)
            shoot_group.add(fireball)

    # Класс снаряда
    class Fireball(pygame.sprite.Sprite):
        def __init__(self, x, y, speedx, speedy):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/projectright1.png")
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y
            self.speedx = speedx
            self.speedy = speedy

        def update (self):

            # Движение и спрайты
            self.rect.x += self.speedx
            self.rect.y += self.speedy

            if self.speedx > 0:
                self.image = pygame.image.load("pictures/projectright1.png")
            if self.speedx < 0:
                self.image = pygame.image.load("pictures/projectleft1.png")
            if self.speedy < 0:
                self.image = pygame.image.load("pictures/projectup1.png")
            if self.speedy > 0:
                self.image = pygame.image.load("pictures/projectdown1.png")

            # Коллизии со стенами
            for block in collis:
                block = block[0]
                if self.rect.colliderect(block):
                    self.kill()

            # Коллизии с границей
            if self.rect.right > 960:
                self.kill()
            if self.rect.left < 0:
                self.kill()
            if self.rect.bottom > 960:
                self.kill()
            if self.rect.top < 0:
                self.kill()

    # Класс врага
    class Enemy(pygame.sprite.Sprite):
        def __init__(self, spawncoordx, spawncoordy):  # Создание спрайта
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/troop1.png")  # создание изображение
            self.rect = self.image.get_rect()  # создание прямоугольника для манипуляции с изображением
            self.rect.left = 0  # Положение прямоугольника
            self.rect.centerx = spawncoordx
            self.rect.centery = spawncoordy
            self.speedx = 0
            self.speedy = 0
            self.mctop = mc.rect.top
            self.mcbottom = mc.rect.bottom
            self.mcright = mc.rect.right
            self.mcleft = mc.rect.left
            self.mc = mc

        def update(self):
            # Интелект и коллизии со стенами
            if self.rect.top > self.mcbottom:
                self.speedy = enemyspeed
                self.rect.y -=self.speedy
                for block in collis:
                    block = block[0]
                    if self.rect.colliderect(block):
                        self.rect.top = block.bottom
            if self.rect.bottom < self.mctop:
                self.speedy = enemyspeed
                self.rect.y += self.speedy
                for block in collis:
                    block = block[0]
                    if self.rect.colliderect(block):
                        self.rect.bottom = block.top
            if self.rect.right < self.mcleft:
                self.speedx = enemyspeed
                self.rect.x += self.speedx
                for block in collis:
                    block = block[0]
                    if self.rect.colliderect(block):
                        self.rect.right = block.left
            if self.rect.left > self.mcright:
                self.speedx = enemyspeed
                self.rect.x -= self.speedx
                for block in collis:
                    block = block[0]
                    if self.rect.colliderect(block):
                        self.rect.left = block.right
            if (frame // 10) % 2 == 0:
                self.image = pygame.image.load("pictures/troop1.png")
            else:
                self.image = pygame.image.load("pictures/troop2.png")

    # Уровень
    level1 = ["@@@@@##@@@@@",
              "@##########@",
              "@##########@",
              "@##########@",
              "@##########@",
              "#####@@#####",
              "#####@@#####",
              "@##########@",
              "@##########@",
              "@##########@",
              "@##########@",
              "@@@@@##@@@@@",]

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

    # Группы спрайтов
    mc_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    shoot_group = pygame.sprite.Group()
    mc = MC()
    mc_group.add(mc)

    # Логика игры
    while True:
        clock.tick(60)
        if frame > 60:
            frame = 0
        frame = frame + 1
        lastarrowx = '0'
        lastarrowy = '0'
        spawnpos = randint(1, 4)

        # Спавн врагов
        if frame == 1:
            if spawnpos == 1:
                enemy = Enemy(500, 0)
                enemy_group.add(enemy)
            if spawnpos == 2:
                enemy = Enemy(500, 980)
                enemy_group.add(enemy)
            if spawnpos == 3:
                enemy = Enemy(0, 500)
                enemy_group.add(enemy)
            if spawnpos == 4:
                enemy = Enemy(980, 500)
                enemy_group.add(enemy)

        # Логика клавиш
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            enemyspeed = 3
            playerspeed = 5
            projectspeedx = 15
            projectspeedy = 15
            playerspeedmem = playerspeed
            keystate = pygame.key.get_pressed()

            #Контроль скорости по диоганали
            if (keystate[pygame.K_a] and keystate[pygame.K_w]) or (
                    keystate[pygame.K_a] and keystate[pygame.K_s]) or (
                    keystate[pygame.K_d] and keystate[pygame.K_w]) or (
                    keystate[pygame.K_d] and keystate[pygame.K_s]):
                playerspeed = playerspeed / 1.5
            else:
                playerspeed = playerspeedmem

            # Стрельба
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    projectspeedx = projectspeedx
                    projectspeedy -= projectspeedy
                    lastarrowx = 'right'
                    mc.shoot()
                if event.key == pygame.K_LEFT:
                    projectspeedx = -projectspeedx
                    projectspeedy -= projectspeedy
                    lastarrowx = 'left'
                    mc.shoot()
                if event.key == pygame.K_UP:
                    projectspeedx -= projectspeedx
                    projectspeedy = -projectspeedy
                    lastarrowy = 'up'
                    mc.shoot()
                if event.key == pygame.K_DOWN:
                    projectspeedx -= projectspeedx
                    projectspeedy = projectspeedy
                    lastarrowy = 'down'
                    mc.shoot()
                if lastarrowy == 'up' and lastarrowx == 'right':
                    projectspeedx = projectspeedx
                    projectspeedy = -projectspeedy
                    mc.shoot()
                if lastarrowy == 'up' and lastarrowx == 'left':
                    projectspeedx = -projectspeedx
                    projectspeedy = -projectspeedy
                    mc.shoot()
                if lastarrowy == 'down' and lastarrowx == 'right':
                    projectspeedx = projectspeedx
                    projectspeedy = projectspeedy
                    mc.shoot()
                if lastarrowy == 'down' and lastarrowx == 'left':
                    projectspeedx = -projectspeedx
                    projectspeedy = -projectspeedy
                    mc.shoot()

        # обновление спрайтов
        mc_group.update()
        shoot_group.update()
        enemy_group.update()

        #Логика столкновений
        pygame.sprite.groupcollide(shoot_group,enemy_group, True, True)
        pygame.sprite.groupcollide(enemy_group,mc_group, True, True)

        # Отрисовка всего
        screen.fill((202, 220, 159))
        for block in collis:
            screen.blit(block[1], block[0])
        shoot_group.draw(screen)
        mc_group.draw(screen)  # прорисовка спрайта
        enemy_group.draw(screen)
        pygame.display.flip()  # обновление окна

base()
