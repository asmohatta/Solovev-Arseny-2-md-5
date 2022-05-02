import pygame
import sys
from random import randint

PROJECT_SPEED_X = 7
PROJECT_SPEED_Y = 7

def base():
    pygame.init()
    clock = pygame.time.Clock()
    frame = 0
    seconds = 0
    lvlcount = 1
    finallvl = 0
    bosshp = 5
    killcount = 30
    screencount = 0
    enemyspeed = 3
    playerspeed = 5
    projectspeedx = 0
    projectspeedy = 0
    keystate = pygame.key.get_pressed()
    screen = pygame.display.set_mode((960, 960))
    pygame.display.set_caption("Underground menace")
    screen.fill((202, 220, 159))
    pygame.display.flip()

    class MC(pygame.sprite.Sprite):  # Класс главного героя
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/MC.png")
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y
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

        def update(self):

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
            self.mctop = mc.rect.top
            self.mcbottom = mc.rect.bottom
            self.mcright = mc.rect.right
            self.mcleft = mc.rect.left
            self.mccenterx = mc.rect.centerx
            self.mccentery = mc.rect.centery

            # Интелект и коллизии со стенами
            if self.rect.centery > self.mccentery:
                self.speedy = enemyspeed
                self.rect.y -= self.speedy
                for block in collis:
                    block = block[0]
                    if self.rect.colliderect(block):
                        self.rect.top = block.bottom
            if self.rect.centery < self.mccentery:
                self.speedy = enemyspeed
                self.rect.y += self.speedy
                for block in collis:
                    block = block[0]
                    if self.rect.colliderect(block):
                        self.rect.bottom = block.top
            if self.rect.centerx < self.mccenterx:
                self.speedx = enemyspeed
                self.rect.x += self.speedx
                for block in collis:
                    block = block[0]
                    if self.rect.colliderect(block):
                        self.rect.right = block.left
            if self.rect.centerx > self.mccenterx:
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

        def death(self, deathframe):
            self.deathframe = deathframe
            collectible = Collectible(self.rect.centerx, self.rect.centery)
            collectible_group.add(collectible)
            self.kill()

    class Boss(pygame.sprite.Sprite):
        def __init__(self):  # Создание спрайта
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/Demon1.png")  # создание изображение
            self.rect = self.image.get_rect()  # создание прямоугольника для манипуляции с изображением
            self.rect.top = 80  # Положение прямоугольника
            self.rect.right = 880
            self.speedy = 5
        def update(self):
            if self.rect.top == 80:
                self.speedy = 5
            if self.rect.bottom == 880:
                self.speedy = -5
            self.rect.y += self.speedy
        def bossfire(self):
            fireball = Fireball(self.rect.centerx, self.rect.centery, -10, 0)
            bossshoot_group.add(fireball)

    #Интерфейс
    class HUD(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/interface.png")
            self.rect = self.image.get_rect()
            self.rect.centerx = 480
            self.rect.centery = 200
        def closetutor(self):
            self.kill()
        def theend(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/loose.png")
            self.rect = self.image.get_rect()
            self.rect.centerx = 480
            self.rect.centery = 480
        def win(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/win.png")
            self.rect = self.image.get_rect()
            self.rect.centerx = 480
            self.rect.centery = 200

    class Collectible(pygame.sprite.Sprite):
        def __init__(self, centerx, centery):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/Collect.png")
            self.rect = self.image.get_rect()
            self.centerx = centerx
            self.centery = centery
        def update(self):
            self.rect.centerx = self.centerx
            self.rect.centery = self.centery

    class Sword(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/Sword.png")
            self.rect = self.image.get_rect()
            self.rect.centerx = 920
            self.rect.centery = 480

    # Уровни
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

    level2 = ["@@@@@##@@@@@",
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
              "@@@@@##@@@@@", ]

    level3 = ["@@@@@##@@@@@",
              "@##########@",
              "@##########@",
              "@####@@####@",
              "@##########@",
              "###@####@###",
              "###@####@###",
              "@##########@",
              "@####@@####@",
              "@##########@",
              "@##########@",
              "@@@@@##@@@@@", ]

    level4 = ["@@@@@##@@@@@",
              "@##########@",
              "@##########@",
              "@##########@",
              "@##########@",
              "@##@#@@####@",
              "@##########@",
              "@#######@##@",
              "@@########@@",
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

    # Группы спрайтов
    mc_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    shoot_group = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()
    bossshoot_group = pygame.sprite.Group()
    collectible_group = pygame.sprite.Group()
    hud_group = pygame.sprite.Group()
    sword_group = pygame.sprite.Group()
    sword = Sword()
    hud = HUD()
    boss = Boss()
    mc = MC(480, 480)
    hud_group.add(hud)
    mc_group.add(mc)

    # Логика игры
    while True:
        clock.tick(60)
        if frame > 60:
            frame = 0
            seconds += 1
        frame = frame + 1

        if screencount == 0:
            screen.fill((202, 220, 159))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        screencount = 1

        if screencount == 1:
            if seconds > 5:
                hud.closetutor()
            if killcount == 0:
                if lvlcount == 1:
                    collis = levelmaker(level2)
                    enemy_group.empty()
                    shoot_group.empty()
                    mc.rect.centerx = 480
                    mc.rect.centery = 350
                if lvlcount == 2:
                    collis = levelmaker(level3)
                    enemy_group.empty()
                    shoot_group.empty()
                    mc.rect.centerx = 480
                    mc.rect.centery = 480
                if lvlcount == 3:
                    collis = levelmaker(level4)
                    enemy_group.empty()
                    shoot_group.empty()
                    boss_group.add(boss)
                    mc.rect.centerx = 200
                    mc.rect.centery = 480
                killcount = 30
                lvlcount += 1
                if lvlcount > 3:
                    finallvl = 1

            if frame % 15 == 0 and finallvl == 1 and bosshp > 0:
                boss.bossfire()

            # Спавн врагов
            spawnpos = randint(1, 4)
            if frame == 1 and lvlcount < 4:
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
                projectspeedx = 0
                projectspeedy = 0
                playerspeedmem = playerspeed
                keystate = pygame.key.get_pressed()

                # Контроль скорости по диоганали
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
                        projectspeedx = PROJECT_SPEED_X
                        projectspeedy = 0
                        mc.shoot()
                    elif event.key == pygame.K_LEFT:
                        projectspeedx = -PROJECT_SPEED_X
                        projectspeedy = 0
                        mc.shoot()
                    elif event.key == pygame.K_UP:
                        projectspeedx = 0
                        projectspeedy = -PROJECT_SPEED_Y
                        mc.shoot()
                    elif event.key == pygame.K_DOWN:
                        projectspeedx = 0
                        projectspeedy = PROJECT_SPEED_Y
                        mc.shoot()

            # обновление спрайтов
            hud_group.update()
            mc_group.update()
            shoot_group.update()
            enemy_group.update()
            boss_group.update()
            bossshoot_group.update()
            collectible_group.update()
            shoot_group.update()

            # Логика столкновений
            if pygame.sprite.groupcollide(shoot_group, enemy_group, True, True):
                killcount -= 1
            if pygame.sprite.groupcollide(enemy_group, mc_group, True, True):
                screencount = 2
            pygame.sprite.groupcollide(bossshoot_group, mc_group, True, True)
            if pygame.sprite.groupcollide(shoot_group, boss_group, True, False):
                bosshp -= 1
                if bosshp == 0:
                    boss.kill()
                    sword_group.add(sword)
            if pygame.sprite.groupcollide(mc_group, sword_group, False, False):
                pygame.quit
                sys.exit()

            # Отрисовка всего
            screen.fill((202, 220, 159))
            for block in collis:
                screen.blit(block[1], block[0])
            hud_group.draw(screen)
            sword_group.draw(screen)
            shoot_group.draw(screen)
            mc_group.draw(screen)  # прорисовка спрайта
            enemy_group.draw(screen)
            collectible_group.draw(screen)
            boss_group.draw(screen)
            bossshoot_group.draw(screen)
            pygame.display.flip()  # обновление окна

    if screencount == 2:
        screen.fill((202, 220, 159))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screencount = 1

base()
