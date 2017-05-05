!#/usr/bin/env python3

import pygame
import math

class GameSpace:
    def main(self):
        pygame.init()
        self.size = self.width,self.height = 640,480
        self.black = 0,0,0
        self.screen = pygame.display.se_mode(self.siz)

        while_loop = 1
        self.clock = pygame.time.Clock()

        pygame.key.set_repeat(1,1)
        while while_loop:
            self.clock.tick(60)
            for even in pygame.event.get()
                if event.type == pygame.QUIT:
                    while_loop =0
                    break

            self.screen.fill(self.black)

            pygame.display.flip()

if __name__ == "__main__":
    gs = GameSpace()
    gs.main()
