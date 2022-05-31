import pygame
import sys
from random import randint

PROJECT_SPEED_X = 7
PROJECT_SPEED_Y = 7
KILLCOUNT = 30

def base():
    pygame.init()
    clock = pygame.time.Clock()
    frame = 0
    seconds = 0
    lvlcount = 0
    finallvl = 0
    bosshp = 5
    killcount = KILLCOUNT
    screencount = 0
    enemyspeed = 3
    playerspeed = 5
    projectspeedx = 0
    projectspeedy = 0
    keystate = pygame.key.get_pressed()
    update = True
    enemies = 0
    musicstart=0
    font = pygame.font.Font("Arcadianarcade-Regular.otf",80)
    screen = pygame.display.set_mode((960, 960))
    pygame.display.set_caption("Sword Quest")
    screen.fill((202, 220, 159))
    pygame.display.flip()

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
              "@###@##@###@",
              "@##@####@##@",
              "############",
              "############",
              "@##@####@##@",
              "@###@##@###@",
              "@##########@",
              "@##########@",
              "@@@@@##@@@@@", ]

    level5 = ["@@@@@##@@@@@",
              "@#@@####@@#@",
              "@@@######@@@",
              "@@########@@",
              "@##########@",
              "#####@@#####",
              "#####@@#####",
              "@##########@",
              "@@########@@",
              "@@@######@@@",
              "@#@@####@@#@",
              "@@@@@##@@@@@", ]

    level4 = ["@@@@@##@@@@@",
              "@#@@@##@@@#@",
              "@##########@",
              "@##@@##@@##@",
              "@##########@",
              "############",
              "############",
              "@##########@",
              "@##@@##@@##@",
              "@##########@",
              "@#@@@##@@@#@",
              "@@@@@##@@@@@", ]

    level6 = ["@@@@@##@@@@@",
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
            if not (keystate[pygame.K_w]) and not (keystate[pygame.K_s]) and \
                    not (keystate[pygame.K_a]) and not (keystate[pygame.K_d]):
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
            self.dir1 = 0
            self.dir2 = 0

        def update(self):
            self.mctop = mc.rect.top
            self.mcbottom = mc.rect.bottom
            self.mcright = mc.rect.right
            self.mcleft = mc.rect.left
            self.mccenterx = mc.rect.centerx
            self.mccentery = mc.rect.centery
            self.speedy = enemyspeed
            self.speedx = enemyspeed

            # Интелект и коллизии со стенами
            if self.rect.centery > self.mccentery:
                self.dir1 = 1
                self.rect.y -= self.speedy
                for block in collis:
                    block = block[0]
                    if self.rect.colliderect(block):
                        self.rect.top = block.bottom
            if self.rect.centery < self.mccentery:
                self.dir1 = 2
                self.rect.y += self.speedy
                for block in collis:
                    block = block[0]
                    if self.rect.colliderect(block):
                        self.rect.bottom = block.top
            if self.rect.centerx < self.mccenterx:
                self.dir2 = 1
                self.rect.x += self.speedx
                for block in collis:
                    block = block[0]
                    if self.rect.colliderect(block):
                        self.rect.right = block.left
            if self.rect.centerx > self.mccenterx:
                self.dir2 = 2
                self.rect.x -= self.speedx
                for block in collis:
                    block = block[0]
                    if self.rect.colliderect(block):
                        self.rect.left = block.right

            if (self.dir1<0 and self.dir1<0):
                self.speedx = self.speedx/1.5
                self.speedy = self.speedy/1.5
            if (frame // 10) % 2 == 0:
                self.image = pygame.image.load("pictures/troop1.png")
            else:
                self.image = pygame.image.load("pictures/troop2.png")


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

    class THEEND(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/Death screen.png")
            self.rect = self.image.get_rect()
            self.rect.top = 0
            self.rect.left = 0

    class WIN(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/win screen.png")
            self.rect = self.image.get_rect()
            self.rect.top = 0
            self.rect.left = 0

    class Title(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/Title screen.png")
            self.rect = self.image.get_rect()
            self.rect.top = 0
            self.rect.left = 0

    class Sword(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("pictures/Sword.png")
            self.rect = self.image.get_rect()
            self.rect.centerx = 920
            self.rect.centery = 480

    def levelmaker(level):
        global texture, mc
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
    hud_group = pygame.sprite.Group()
    sword_group = pygame.sprite.Group()
    sword = Sword()
    hud = HUD()
    boss = Boss()
    hud_group.add(hud)

    # Логика игры
    while True:
        clock.tick(60)
        if frame > 60:
            frame = 0
            seconds += 1
        frame = frame + 1

        if screencount == 0:
            screen.fill((202, 220, 159))
            title = Title()
            sword_group.add(title)
            sword_group.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        screencount = 1
                        sword_group.empty()

        if screencount == 1:
            if update == True:
                mc = MC(480,480)
                mc_group.add(mc)
                seconds = 0
                killcount = KILLCOUNT
                update = False
            if seconds > 5:
                hud.closetutor()
            if killcount == 0:
                lvlcount += 1
                if lvlcount == 1:
                    collis = levelmaker(level2)
                    enemy_group.empty()
                    enemies = 0
                    shoot_group.empty()
                    mc_group.empty()
                    mc = MC(480,350)
                    mc_group.add(mc)
                if lvlcount == 2:
                    collis = levelmaker(level3)
                    enemy_group.empty()
                    enemies = 0
                    shoot_group.empty()
                    mc_group.empty()
                    mc = MC(480, 480)
                    mc_group.add(mc)
                if lvlcount == 3:
                    collis = levelmaker(level4)
                    enemy_group.empty()
                    enemies = 0
                    shoot_group.empty()
                    mc_group.empty()
                    mc = MC(480, 480)
                    mc_group.add(mc)
                if lvlcount == 4:
                    collis = levelmaker(level5)
                    enemy_group.empty()
                    enemies = 0
                    shoot_group.empty()
                    mc_group.empty()
                    mc = MC(480, 350)
                    mc_group.add(mc)
                if lvlcount == 5:
                    collis = levelmaker(level6)
                    enemy_group.empty()
                    enemies = 0
                    shoot_group.empty()
                    boss_group.add(boss)
                    mc_group.empty()
                    mc = MC(200, 480)
                    mc_group.add(mc)
                killcount = KILLCOUNT
                if lvlcount > 4:
                    finallvl = 1

            if frame % 15 == 0 and finallvl == 1 and bosshp > 0:
                boss.bossfire()

            # Спавн врагов
            spawnpos = randint(1, 4)
            if frame == 1 and lvlcount < 5:
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
                enemies += 1

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
            shoot_group.update()

            # Логика столкновений
            if pygame.sprite.groupcollide(shoot_group, enemy_group, True, True):
                killcount -= 1
                enemies -= 1
            if pygame.sprite.groupcollide(enemy_group, mc_group, True, True):
                screencount = 2
                musicstart = 0
                continue
            if pygame.sprite.groupcollide(bossshoot_group, mc_group, True, True):
                screencount = 2
                continue
            if pygame.sprite.groupcollide(shoot_group, boss_group, True, False):
                bosshp -= 1
                if bosshp == 0:
                    boss.kill()
                    sword_group.add(sword)
            if pygame.sprite.groupcollide(mc_group, sword_group, False, False):
                screencount = 3
                musicstart=0
                continue

            # Отрисовка всего
            screen.fill((202, 220, 159))
            for block in collis:
                screen.blit(block[1], block[0])
            hud_group.draw(screen)
            text1 = font.render(str(killcount), False, (47,98,47))
            if lvlcount < 6:
                screen.blit(text1, (82, 810))
            sword_group.draw(screen)
            shoot_group.draw(screen)
            mc_group.draw(screen)  # прорисовка спрайта
            enemy_group.draw(screen)
            boss_group.draw(screen)
            bossshoot_group.draw(screen)
            if musicstart == 0:
                pygame.mixer.music.load("Sewer Surfin'.mp3")
                pygame.mixer.music.play(5)
                musicstart = 1
            pygame.display.flip()  # обновление окна

        #Экран смерти
        if screencount == 2:
            screen.fill((202, 220, 159))
            theend = THEEND()
            if musicstart == 0:
                pygame.mixer.music.unload()
                pygame.mixer.music.load("Game Over.mp3")
                pygame.mixer.music.play()
                musicstart = 1
            hud_group.empty()
            hud_group.add(theend)
            hud_group.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        screencount = 1
                        update = True
                        enemy_group.empty()
                        enemies = 0
                        shoot_group.empty()
                        boss_group.empty()
                        bossshoot_group.empty()
                        finallvl = 0
                        lvlcount = 0
                        musicstart = 0
                        killcount = KILLCOUNT
                        collis = levelmaker(level1)
                        hud_group.empty()
                        continue

        #Финальный экран
        if screencount == 3:
            screen.fill((202, 220, 159))
            win = WIN()
            if musicstart == 0:
                pygame.mixer.music.unload
                pygame.mixer.music.load("Epilogue.mp3")
                pygame.mixer.music.play()
                musicstart = 1
            hud_group.empty()
            hud_group.add(win)
            hud_group.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

base()
