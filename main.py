#!/usr/bin/env python3

import pygame
import math

class Background:
    def __init__(self):
        self.image = pygame.image.load("graphics/background.png")
        self.rect = self.image.get_rect()

class GameSpace:
    def main(self):
        pygame.init()
        self.size = self.width,self.height = 640,480
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)

        #image classes
        self.bg = Background()

        while_loop = 1
        self.clock = pygame.time.Clock()

        pygame.key.set_repeat(1,1)
        while while_loop:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    while_loop =0
                    break

            self.screen.fill(self.black)
            self.screen.blit(self.bg.image, self.bg.rect)

            pygame.display.flip()

if __name__ == "__main__":
    gs = GameSpace()
    gs.main()
