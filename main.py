#!/usr/bin/env python3

import pygame
import math
import random

class Background:
    def __init__(self):
        self.image = pygame.image.load("graphics/background.png")
        self.rect = self.image.get_rect()

class Player:
    def __init__(self, image_file):
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (64, 48))
        self.score = 0

    def move(self):

        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT]:
            self.rect.centerx += 5
        elif key[pygame.K_LEFT]:
            self.rect.centerx -= 5
        elif key[pygame.K_UP]:
            self.rect.centery -= 5
        elif key[pygame.K_DOWN]:
            self.rect.centery += 5

    #def get_player_score(self):


class Rupee:
    def __init__(self, gs, player):
        self.image = pygame.image.load("graphics/rupee.png")
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (64, 48))
        self.player = player
        self.gs = gs

    def return_rupee_pos(self):
        pos = random.randint(1, 7)
        
        possible_positions = {
                1 : (30,100), 
                2 : (100, 300),
                3 : (350, 20),
                4 : (600, 400),
                5 : (320, 240),
                6 : (400, 40),
                7 : (200, 170)
        }

        self.rect.x = possible_positions[pos][0]
        self.rect.y = possible_positions[pos][1]
        
        return possible_positions[pos][0], possible_positions[pos][1]

    def found(self):
        if self.player.rect.centerx < self.rect.centerx + 5 and self.player.rect.centerx > self.rect.centerx - 5 and self.player.rect.centery < self.rect.centery + 5 and self.player.rect.centery > self.rect.centery - 5:
                
                print("FOUND")
                #self.player.update_score()
                self.rect.x, self.rect.y = self.return_rupee_pos()
                self.gs.screen.blit(self.image, self.rect)

    def tick(self):
        self.found()

class GameSpace:
    def main(self):
        pygame.init()
        self.size = self.width,self.height = 640,480
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)

        #image classes
        self.bg = Background()
        
        self.link = Player("graphics/link.png")
        self.link.rect.x = 320
        self.link.rect.y = 420

        self.rupee1 = Rupee(self, self.link)
        self.rupee1.rect.x, self.rupee1.rect.y = self.rupee1.return_rupee_pos()

        self.rupee2 = Rupee(self, self.link)
        self.rupee2.rect.x, self.rupee2.rect.y = self.rupee2.return_rupee_pos()

        while_loop = 1
        self.clock = pygame.time.Clock()

        pygame.key.set_repeat(1,1)
        while while_loop:
            time_counter = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    while_loop = 0
                    break

            self.link.move()

            #print(time_counter)

            self.rupee1.tick()
            self.rupee2.tick()

            self.screen.fill(self.black)
            self.screen.blit(self.bg.image, self.bg.rect)
            self.screen.blit(self.rupee1.image, self.rupee1.rect)
            self.screen.blit(self.rupee2.image, self.rupee2.rect)
            self.screen.blit(self.link.image, self.link.rect)

            if time_counter > 1000:
                self.rupee1.rect.x, self.rupee1.rect.y = self.rupee1.return_rupee_pos()
                self.rupee2.rect.x, self.rupee2.rect.y = self.rupee2.return_rupee_pos()
                time_counter = 0

            pygame.display.flip()

if __name__ == "__main__":
    gs = GameSpace()
    gs.main()
