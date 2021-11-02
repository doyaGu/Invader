import pygame, sys
from pygame.locals import *


def getNewSideEnemy():
    indexOfEnemies = (i for i in enumerate(enemies))
    sortedIndex = sorted(list(indexOfEnemies), key=lambda x: x[1].left)
    if len(enemies) == 0:
        return 0, 0
    else:
        return sortedIndex[0][0], sortedIndex[len(sortedIndex) - 1][0]


pygame.init()
mainClock = pygame.time.Clock()
FPS = 60

size = width, height = 600, 500
windowSurface = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("Invader")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

basicFont = pygame.font.SysFont(None, 48)

score = 0
player = pygame.Rect(300, 450, 60, 15)
bullets = []
enemies = [pygame.Rect(left, top, 30, 30) for top in range(60, 360, 60) for left in range(60, 540, 60)]
moveLeft = False
moveRight = False
firing = False
speed = [8, 6, 1]

state = 0
leftest = 0
rightest = 7

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == ord('a'):
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = True
                moveLeft = False
            if event.key == K_SPACE:
                firing = True

        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = False

    windowSurface.fill(BLACK)

    if moveLeft and player.left > 0:
        player.left -= speed[0]
    if moveRight and player.right < width:
        player.right += speed[0]
    if firing:
        bullets.append(pygame.Rect(player.left + player.width / 2, player.top - 20, 5, 20))
        firing = False

    pygame.draw.rect(windowSurface, WHITE, player)

    if len(enemies) != 0:
        if enemies[leftest].left > 20 and enemies[rightest].right < 580:
            if state == 0:
                for i in enemies[:]:
                    i.left -= speed[2]
            if state == 1:
                for i in enemies[:]:
                    i.left += speed[2]
            if state == 2:
                for i in enemies[:]:
                    i.left -= speed[2]
        elif enemies[leftest].left <= 20 and enemies[rightest].right < 580:
            for i in enemies[:]:
                i.left += speed[2]
            state = 1
        elif enemies[leftest].left > 20 and enemies[rightest].right >= 580:
            for i in enemies[:]:
                i.left -= speed[2]
            state = 2

    for enemy in enemies[:]:
        for bullet in bullets[:]:
            if bullet.top < 0:
                bullets.remove(bullet)
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1

                leftest, rightest = getNewSideEnemy()

        text = basicFont.render(str(score), True, WHITE, BLACK)

    for i in range(len(enemies)):
        pygame.draw.rect(windowSurface, BLUE, enemies[i])

    for i in range(len(bullets)):
        pygame.draw.rect(windowSurface, GRAY, bullets[i])
        bullets[i].top -= speed[1]

    windowSurface.blit(text, (0, 0))

    pygame.display.update()
    mainClock.tick(FPS)
