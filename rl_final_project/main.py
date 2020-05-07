import pygame
from Grid import Grid
from consts import SCREEN_SIZE
import agent

pygame.init()
pygame.display.set_caption('2048')
pygame.font.init()
clock = pygame.time.Clock()
clock.tick(60)

screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])
screen.fill((127, 127, 127))


g = Grid(pygame, screen)
a = agent.agent()
running = True
agent_playing = False
g.render()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                agent_playing = not agent_playing 
                g.reset(hardreset=True)
                break
            if event.key == pygame.K_r:
                g.reset()
                g.render()
                break

            if not agent_playing:
                g.move(event.key)
                g.render()
                if g.is_win():
                    print(g.score, g.highscore)
                elif g.is_gameover():
                    print(g.score, g.highscore)


    if agent_playing:
        a.step(g)
        a.render(g)

pygame.quit()