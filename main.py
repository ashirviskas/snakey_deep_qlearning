import pygame
import random
import sys
from pygame.locals import *
import numpy as np


WALL_COLLISION = -1


def collide(a, b, walls):
    if a[0] == b[0] and a[1] == b[1]:
        return 1
    else:
        if -1 < a[0] < walls[0] and -1 < a[1] < walls[1]:
            return 0
        else:
            return WALL_COLLISION


def self_collide(snake):
    for i, s in enumerate(snake):
        for j in range(i + 1, len(snake)):
            if s[0] == snake[j][0] and s[1] == snake[j][1]:
                return True
    return False


def die(screen, score):
    f = pygame.font.SysFont('Arial', 30)
    t = f.render('Your score was: ' + str(score), True, (0, 0, 0))
    screen.blit(t, (10, 270))
    pygame.display.update()
    pygame.time.wait(2000)
    sys.exit(0)


def put_food():
    applepos = [random.randint(0, 59), random.randint(0, 59)]
    return applepos


def game_loop(s, walls, initial_snakepos):
    snakepos = initial_snakepos
    clock = pygame.time.Clock()
    apple_pos = put_food()
    score = 0
    dirs = 0
    gameboard = np.zeros(shape=(walls[0], walls[1]), dtype=np.int)
    f = pygame.font.SysFont('Arial', 20)
    while True:
        clock.tick(10)
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit(0)
            elif e.type == KEYDOWN:
                if e.key == K_UP and dirs != 0:
                    dirs = 2
                elif e.key == K_DOWN and dirs != 2:
                    dirs = 0
                elif e.key == K_LEFT and dirs != 1:
                    dirs = 3
                elif e.key == K_RIGHT and dirs != 3:
                    dirs = 1
        collision = collide(snakepos[0], apple_pos, walls)
        if self_collide(snakepos):
            die(s, score)
        if collision == 1:
            score += 1
            snakepos.append([100, 100])
            apple_pos = put_food()
        elif collision == WALL_COLLISION:
            die(s, score)
        elif collision == 0:
            pass
        s.fill((255, 255, 255))

        for i in range(len(snakepos)-1, 0, -1):
            print("SS")
            print(i, snakepos[i], snakepos[i - 1])
            snakepos[i] = list(snakepos[i - 1])

        if dirs == 0:
            snakepos[0][1] += 1
        elif dirs == 1:
            snakepos[0][0] += 1
        elif dirs == 2:
            snakepos[0][1] -= 1
        elif dirs == 3:
            snakepos[0][0] -= 1

        for snekbit in snakepos:
            gameboard[snekbit[0], snekbit[1]] = 1
            # s.blit(snek_img, (snekbit[0], snekbit[1]))
        gameboard[snakepos[0][0], snakepos[0][1]] = 10
        gameboard[apple_pos[0], apple_pos[1]] = 100
        # s.blit(apple_img, (apple_pos[0], apple_pos[1]))
        t = f.render(str(score), True, (0, 75, 75))
        Z = 255 * gameboard / gameboard.max()
        Z = Z.repeat(10, axis=0).repeat(10, axis=1)
        surf = pygame.surfarray.make_surface(Z)
        gameboard.fill(0)
        s.blit(surf, (0, 0))
        s.blit(t, (10, 10))
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    s = pygame.display.set_mode((600, 600))
    apple_img = pygame.Surface((1, 1))
    apple_img.fill((0, 255, 0))
    snek_img = pygame.Surface((1, 1))
    snek_img.fill((255, 0, 0))
    f = pygame.font.SysFont('Arial', 20)
    snek = [[20, 20], [20, 19]]
    game_loop(s, (60, 60), snek)







