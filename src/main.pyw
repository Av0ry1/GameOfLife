import pygame
import numpy as np

from random import randint

class GameOfLife:
    def __init__(self, fieldSize, screenSize):
        pygame.init()

        self.screen = pygame.display.set_mode(screenSize)
        self.surface = pygame.Surface((fieldSize[0]-2, fieldSize[1]-2))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 24)

        self.screenSize = screenSize
        self.fieldSize = fieldSize
        self.scale = (screenSize[0]/fieldSize[0], screenSize[1]/fieldSize[1])

        self.reset()

        self.paused = 0
        self.tickrate = 5

    def reset(self):
        self.field = np.zeros(self.fieldSize)

        for x in range(10):
            for y in range(10):
                self.field[45+x][45+y] = randint(0, 1)

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused

                if event.key == pygame.K_DOWN:
                    self.tickrate -= 1
                    self.tickrate = max(1, self.tickrate)

                if event.key == pygame.K_UP:
                    self.tickrate += 1

                if event.key == pygame.K_r:
                    self.reset()

    def update(self):
        buf = self.field.copy()

        for x in range(1, self.fieldSize[0]-1):
            for y in range(1, self.fieldSize[1]-1):

                count = buf[x-1][y-1] + buf[x-1][y] + buf[x-1][y+1] + buf[x][y-1] + buf[x][y+1] + buf[x+1][y-1] + buf[x+1][y] + buf[x+1][y+1]

                if 2 <= count <= 3:
                    if count == 3 or buf[x][y]:
                        self.field[x][y] = 1

                else:
                    self.field[x][y] = 0

    def render(self):
        self.screen.fill((10, 10, 12))

        pygame.surfarray.blit_array(self.surface, (self.field*255)[1:self.fieldSize[0]-1, 1:self.fieldSize[1]-1])
        self.screen.blit(pygame.transform.scale(self.surface, (self.screenSize[1]-self.scale[1]*2, self.screenSize[1]-self.scale[1]*2)), self.scale)

        for row, text in enumerate((f'tickrate: {self.tickrate}', '', 'UP/DOWN - tickrate', 'SPACE - pause', 'R - reset')):
            self.screen.blit(self.font.render(text, 1, (240, 240, 250)), (self.screenSize[1], 4+row*20))

        pygame.display.flip()

    def run(self):
        while 1:
            self.clock.tick(self.tickrate)

            self.event()

            if not self.paused:
                self.update()
                
            self.render()

if __name__ == '__main__':
    gameOfLife = GameOfLife((100, 100), (1000, 800))
    gameOfLife.run()